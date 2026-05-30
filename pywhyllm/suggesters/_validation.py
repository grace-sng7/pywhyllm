import asyncio

from .causal_graph import CausalGraph
from .response_models import CausalGraphResponse


class ValidationMixin:
    """
    Causal validation methods — critiquing an existing graph.

    Relies on ``self.client``, ``self.model``, and ``self.context``
    provided by ``ModelSuggester.__init__``.
    """

    async def critique_graph(
        self,
        graph: CausalGraph,
        variables: list[str],
        expertise_list: list[str] | None = None,
        min_confidence: float = 0.5,
    ) -> CausalGraph:
        """
        Get a second opinion on an existing causal graph.

        Shows the LLM the original edges and asks which ones are valid
        direct causal relationships (and whether any are missing).
        Returns a new ``CausalGraph`` representing the critique's view.

        Compare with the original to find confirmed vs disputed edges::

            original = await suggester.suggest_graph(variables, experts)
            critique = await suggester.critique_graph(original, variables, experts)

            for (cause, effect) in original.edges:
                if critique.edge_data(cause, effect):
                    print(f"CONFIRMED: {cause} → {effect}")
                else:
                    print(f"DISPUTED:  {cause} → {effect}")

        Parameters
        ----------
        graph : CausalGraph
            The graph to critique.
        variables : list[str]
            The original variable list.
        expertise_list : list[str] | None
            Expert roles. Multiple experts are queried in parallel.
        min_confidence : float
            Edges below this confidence are dropped before being counted
            as a vote. Default is 0.5.

        Returns
        -------
        CausalGraph
            A new graph containing edges the critique considers valid,
            plus any new edges it suggests.
        """
        edge_descriptions = [
            f"  {cause} → {effect}" for (cause, effect) in graph.edges
        ]
        edge_block = "\n".join(edge_descriptions)

        if not expertise_list:
            response = await self._critique_call(variables, edge_block, expertise=None)
            return CausalGraph.from_responses([response], min_confidence=min_confidence)

        responses = await asyncio.gather(*[
            self._critique_call(variables, edge_block, expertise=expert)
            for expert in expertise_list
        ])
        return CausalGraph.from_responses(list(responses), min_confidence=min_confidence)

    async def _critique_call(
        self,
        variables: list[str],
        edge_block: str,
        expertise: str | None,
    ) -> CausalGraphResponse:
        system = (
            f"You are an expert in {expertise} studying {self.context}. "
            f"You are reviewing a proposed causal model for correctness."
            if expertise
            else f"You are a helpful assistant reviewing a proposed causal model about {self.context}."
        )
        return await self.client.chat.completions.create(
            **self._api_kwargs,
            response_model=CausalGraphResponse,
            messages=[
                {"role": "system", "content": system},
                {
                    "role": "user",
                    "content": (
                        f"A causal model has been proposed with these variables: {variables}\n\n"
                        f"The proposed causal edges are:\n{edge_block}\n\n"
                        f"Review each edge. Think step by step about whether each represents "
                        f"a valid, direct causal relationship. "
                        f"Return only the edges you believe are correct. "
                        f"Also add any direct causal edges you believe are missing. "
                        f"Do not include indirect relationships or feedback loops."
                    ),
                },
            ],
        )
