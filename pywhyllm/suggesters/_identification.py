import asyncio

from .response_models import (
    ConfoundingFactorsResponse,
    LatentConfoundersResponse,
    NegativeControlsResponse,
)


class IdentificationMixin:
    """
    Causal identification methods — confounders, negative controls.

    Relies on ``self.client``, ``self.model``, and ``self.context``
    provided by ``ModelSuggester.__init__``.
    """

    # ------------------------------------------------------------------
    # Confounders
    # ------------------------------------------------------------------

    async def suggest_confounders(
        self,
        treatment: str,
        outcome: str,
        variables: list[str],
        expertise_list: list[str] | None = None,
        latent: bool = False,
    ) -> list[str]:
        """
        Suggest confounders of the treatment → outcome relationship.

        Parameters
        ----------
        treatment : str
        outcome : str
        variables : list[str]
            Candidate variables to search within (ignored when ``latent=True``).
        expertise_list : list[str] | None
            Expert roles. Multiple experts are queried in parallel; results
            are unioned and deduplicated.
        latent : bool
            ``False`` (default): find confounders within ``variables``.
            ``True``: find unmeasured confounders outside ``variables``.
        """
        if not expertise_list:
            return await self._confounders_call(
                treatment, outcome, variables, expertise=None, latent=latent
            )

        results = await asyncio.gather(*[
            self._confounders_call(treatment, outcome, variables, expertise=expert, latent=latent)
            for expert in expertise_list
        ])

        seen: set[str] = set()
        merged: list[str] = []
        for result in results:
            for c in result:
                if c not in seen:
                    seen.add(c)
                    merged.append(c)
        return merged

    async def _confounders_call(
        self,
        treatment: str,
        outcome: str,
        variables: list[str],
        expertise: str | None,
        latent: bool,
    ) -> list[str]:
        system = (
            f"You are an expert in {expertise} studying {self.context}."
            if expertise
            else "You are a helpful assistant for causal reasoning."
        )

        if latent:
            user_content = (
                f"What latent (unmeasured) confounding factors might influence the relationship "
                f"between {treatment} and {outcome}? "
                f"We have already considered the following factors: {variables}. "
                f"Do not repeat them. List only confounding factors not already in that list."
            )
            response = await self.client.chat.completions.create(
                **self._api_kwargs,
                response_model=LatentConfoundersResponse,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user_content},
                ],
            )
            return response.confounding_factors
        else:
            candidates = [v for v in variables if v not in (treatment, outcome)]
            user_content = (
                f"From these factors: {candidates}\n\n"
                f"Which, if any, directly cause both {treatment} and {outcome}? "
                f"Think step by step. Only include factors with a high likelihood of "
                f"confounding the relationship between {treatment} and {outcome}."
            )
            response = await self.client.chat.completions.create(
                **self._api_kwargs,
                response_model=ConfoundingFactorsResponse,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user_content},
                ],
            )
            return [f for f in response.confounding_factors if f in candidates]

    # ------------------------------------------------------------------
    # Negative controls
    # ------------------------------------------------------------------

    async def suggest_negative_controls(
        self,
        treatment: str,
        outcome: str,
        variables: list[str],
        expertise_list: list[str] | None = None,
    ) -> list[str]:
        """
        Suggest negative controls for the treatment → outcome relationship.

        Negative controls are variables that *should* be unaffected by
        changes in the treatment. Useful for robustness checking — if
        your model shows a treatment effect on a negative control,
        something is wrong.

        Parameters
        ----------
        treatment : str
        outcome : str
        variables : list[str]
            Candidate variables to search within.
        expertise_list : list[str] | None
            Expert roles. Multiple experts are queried in parallel.
        """
        if not expertise_list:
            return await self._negative_controls_call(
                treatment, outcome, variables, expertise=None
            )

        results = await asyncio.gather(*[
            self._negative_controls_call(treatment, outcome, variables, expertise=expert)
            for expert in expertise_list
        ])

        seen: set[str] = set()
        merged: list[str] = []
        for result in results:
            for c in result:
                if c not in seen:
                    seen.add(c)
                    merged.append(c)
        return merged

    async def _negative_controls_call(
        self,
        treatment: str,
        outcome: str,
        variables: list[str],
        expertise: str | None,
    ) -> list[str]:
        system = (
            f"You are an expert in {expertise} studying {self.context}."
            if expertise
            else "You are a helpful assistant for causal reasoning."
        )
        candidates = [v for v in variables if v not in (treatment, outcome)]
        user_content = (
            f"From these factors: {candidates}\n\n"
            f"Which, if any, should see zero treatment effect when changing {treatment}? "
            f"Which factors should be completely unaffected by changes in {treatment} "
            f"and are unrelated to the causal mechanisms that affect {outcome}? "
            f"Think step by step. Only include factors you are confident are negative controls."
        )
        response = await self.client.chat.completions.create(
            **self._api_kwargs,
            response_model=NegativeControlsResponse,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user_content},
            ],
        )
        return [f for f in response.negative_controls if f in candidates]
