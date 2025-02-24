from typing import Set, Tuple, Dict, List
from suggesters.protocols import ModelerProtocol
import networkx as nx
import guidance
<<<<<<< Updated upstream:pywhyllm/model_suggester.py
from .helpers import RelationshipStrategy, ModelType
import copy
import random
from enum import Enum
from .prompts import prompts as ps
=======
from guidance import user, system, assistant, gen
from ..helpers import RelationshipStrategy, ModelType
import copy
import random
from enum import Enum
# from ..prompts import prompts as ps
>>>>>>> Stashed changes:pywhyllm/suggesters/model_suggester.py
import os
import re
import csv


class ModelSuggester(ModelerProtocol):
    EXPERTS: list() = [
        "answering questions about causality, you are a helpful causality assistant ",
        "causality, you are an intelligent AI with expertise in causality",
        "cause and effect",
    ]
    CONTEXT: str = """causal mechanisms"""

    def __init__(self, llm):
        if (llm == 'gpt-4'):
            self.llm = guidance.models.OpenAI('gpt-4')

    def suggest_domain_expertises(
<<<<<<< Updated upstream:pywhyllm/model_suggester.py
        self,
        analysis_context,
        factors,
        llm: guidance.llms,
        n_experts: int = 1,
        temperature=0.3,
        model_type: ModelType = ModelType.Completion,
=======
            self,
            analysis_context,
            factors_list,
            n_experts: int = 1,
            temperature=0.3,
            model_type: ModelType = ModelType.Completion,
>>>>>>> Stashed changes:pywhyllm/suggesters/model_suggester.py
    ):
        # suggest = ps[model_type.value]["expertises"]

        expertise_list: List[str] = list()
        success: bool = False

        while not success:
            try:
                # output = suggest(
                #     analysis_context=analysis_context,
                #     factors_list=factors,
                #     n_experts=n_experts,
                #     temperature=temperature
                # )
                lm = self.llm
                with system():
                    lm += "You are a helpful assistant for recommending useful domain expertises."
                with user():
                    lm += f"""What domain expertises have the knowledge and experience needed to identify causal 
                    relationships and causal influences between the {analysis_context}? What domain expertises are 
                    needed to work with and reason about the causal influence between {factors_list}? What domain 
                    expertises have the knowledge and experience to reason and answer questions about influence and 
                    cause between such factors? Think about this in a step by step manner and recommend {n_experts} 
                    expertises and provide each one wrapped within the tags, <domain_expertise></domain_expertise>, 
                    along with the reasoning and explanation wrapped between the tags <explanation></explanation>."""
                with assistant():
                    lm += gen("output", temperature)

                output = lm["output"]
                expertise = re.findall(r"<domain_expertise>(.*?)</domain_expertise>", output)

                if expertise:
                    for i in range(n_experts):
                        expertise_list.append(expertise[i])
                    success = True
                else:
                    # guidance.models.OpenAI.cache.clear()
                    success = False

            except KeyError:
                success = False
                continue

        return expertise_list

<<<<<<< Updated upstream:pywhyllm/model_suggester.py
    def suggest_domain_experts(
        self,
        analysis_context,
        factors,
        llm: guidance.llms,
        n_experts: int = 5,
        temperature=0.3,
        model_type: ModelType = ModelType.Chat,
    ):
        suggest = guidance(ps[model_type.value]["domain_experts"])

        experts_list: Set[str] = set()
        success: bool = False

        while not success:
            try:
                output = suggest(
                    analysis_context=analysis_context,
                    factors_list=factors,
                    n_experts=n_experts,
                    temperature=temperature,
                    llm=llm,
                )
                experts = re.findall(
                    r"<domain_expert>(.*?)</domain_expert>", output["output"]
                )

                if experts:
                    for i in range(n_experts):
                        experts_list.add(experts[i])
                    success = True
                else:
                    llm.OpenAI.cache.clear()
                    success = False

            except KeyError:
                success = False
                continue

        return experts_list

    def suggest_stakeholders(
        self,
        factors,
        llm: guidance.llms,
        n_experts: int = 5,  # must be > 1
        temperature=0.3,
        analysis_context=CONTEXT,
        model_type: ModelType = ModelType.Chat,
=======
    # def suggest_domain_experts(
    #         self,
    #         analysis_context,
    #         factors,
    #         n_experts: int = 5,
    #         temperature=0.3,
    #         model_type: ModelType = ModelType.Chat,
    # ):
    #     suggest = guidance(ps[model_type.value]["domain_experts"])
    #
    #     experts_list: Set[str] = set()
    #     success: bool = False
    #
    #     while not success:
    #         try:
    #             output = suggest(
    #                 analysis_context=analysis_context,
    #                 factors_list=factors,
    #                 n_experts=n_experts,
    #                 temperature=temperature,
    #                 llm=llm,
    #             )
    #             experts = re.findall(
    #                 r"<domain_expert>(.*?)</domain_expert>", output["output"]
    #             )
    #
    #             if experts:
    #                 for i in range(n_experts):
    #                     experts_list.add(experts[i])
    #                 success = True
    #             else:
    #                 llm.OpenAI.cache.clear()
    #                 success = False
    #
    #         except KeyError:
    #             success = False
    #             continue
    #
    #     return experts_list

    def suggest_stakeholders(
            self,
            factors_list,
            n_stakeholders: int = 5,  # must be > 1
            temperature=0.3,
            analysis_context=CONTEXT,
            model_type: ModelType = ModelType.Chat,
>>>>>>> Stashed changes:pywhyllm/suggesters/model_suggester.py
    ):
        # suggest = guidance(ps[model_type.value]["stakeholders"])

        stakeholder_list: List[str] = list()
        success: bool = False

        while not success:
            try:
                lm = self.llm

                with system():
                    lm += "You are a helpful assistant for recommending useful primary and secondary stakeholders."

                with user():
                    lm += f"""What stakeholders have knowledge and experience in and about {analysis_context}? 
                    What stakeholders can work best with and reason well about the causal influence between 
{factors_list}? What stakeholders have the knowledge and experience useful to reason within this context? Think about 
this in a step by step manner and recommend {n_stakeholders} stakeholders. Then provide each useful stakeholder 
wrapped within the tags, <stakeholder></stakeholder>, along with the reasoning and explanation wrapped between the tags
<explanation></explanation>."""
                with assistant():
                    lm += gen("output", temperature)

                output = lm["output"]

                stakeholder = re.findall(r"<stakeholder>(.*?)</stakeholder>", output)
                if stakeholder:
                    for i in range(n_stakeholders):
                        stakeholder_list.append(stakeholder[i])
                    success = True
                else:
                    # llm.OpenAI.cache.clear()
                    success = False

            except KeyError:
                success = False
                continue

        return stakeholder_list

    def suggest_confounders(
<<<<<<< Updated upstream:pywhyllm/model_suggester.py
        self,
        treatment: str,
        outcome: str,
        factors_list: list(),
        llm: guidance.llms,
        experts: list() = EXPERTS,
        analysis_context: list() = CONTEXT,
        stakeholders: list() = None,
        temperature=0.3,
        model_type: ModelType = ModelType.Completion,
=======
            self,
            treatment: str,
            outcome: str,
            factors_list: list(),
            experts: list(),
            domain_expertise,
            analysis_context=CONTEXT,
            stakeholders: list() = None,
            temperature=0.3,
            model_type: ModelType = ModelType.Completion
>>>>>>> Stashed changes:pywhyllm/suggesters/model_suggester.py
    ):

        expert_list: List[str] = list()
        for elements in experts:
            expert_list.append(elements)
        if stakeholders is not None:
            for elements in stakeholders:
                expert_list.append(elements)

        lm = self.llm
        with system():
            lm += f"""You are an expert in {domain_expertise} and are studying {analysis_context}.
You are using your knowledge to help build a causal model that contains all the assumptions about {
            analysis_context}. Where a causal model is a conceptual model that describes the causal mechanisms of a 
        system. You
will do this by by answering questions about cause and effect and using your domain knowledge in {domain_expertise}."""
        with user():
            lm += f"""Follow the next two steps, and complete the first one before moving on to the second: (1) 
                From your perspective as an 
expert in {domain_expertise}, think step by step as you consider the factors that may interact between the {treatment} 
and the {outcome}. Use your knowlegde as an expert in {domain_expertise} to describe the confounders, if there are any 
at all, between the {treatment} and the {outcome}. Be concise and keep your thinking within two paragraphs. Then provide
your step by step chain of thoughts within the tags <thinking></thinking>. (2) From your perspective as an expert in 
{domain_expertise}, which factor(s) of the following factors, if any at all, has/have a high likelihood of directly 
influencing and causing both the assignment of the {treatment} and the {outcome}? Which factor(s) of the following 
factors, 
if any at all, have a causal chain that links to the {treatment} to the {outcome}? Which factor(s) of the following 
factors, 
if any at all, are a confounder to the causal relationship between the {treatment} and the {outcome}? Be concise and 
keep your 
thinking within two paragraphs. Then provide your step by step chain of thoughts within the tags 
<thinking></thinking>. \n factor_names : 
{factors_list} Wrap the name of the factor(s), if any at all, that has/have a high likelihood of directly influencing 
and causing both  the {treatment} and the {outcome}, within the tags 
<confounding_factor>factor_name</confounding_factor> where 
factor_name is one of the items within the factor_names list. If a factor does not have a high likelihood of directly 
confounding, then do not wrap the factor with any tags."""
        with system():
            gen("output", temperature)

        output = lm["output"]

        confounders_edges: Dict[Tuple[str, str], int] = dict()
        confounders_edges[(treatment, outcome)] = 1

        confounders: List[str] = list()

        edited_factors_list: List[str] = []
        for i in range(len(factors_list)):
            if factors_list[i] != treatment and factors_list[i] != outcome:
                edited_factors_list.append(factors_list[i])

        if len(expert_list) > 1:
            for expert in expert_list:
                confounders_edges, confounders_list = self.request_confounders(
                    # suggest=suggest,
                    treatment=treatment,
                    outcome=outcome,
                    analysis_context=analysis_context,
                    expert=expert,
                    edited_factors_list=edited_factors_list,
                    temperature=temperature,
                    # llm=llm,
                    confounders_edges=confounders_edges
                )

                for m in confounders_list:
                    if m not in confounders:
                        confounders.append(m)
        else:
            confounders_edges, confounders_list = self.request_confounders(
                # suggest=suggest,
                treatment=treatment,
                outcome=outcome,
                analysis_context=analysis_context,
                expert=expert_list[0],
                edited_factors_list=edited_factors_list,
                temperature=temperature,
                confounders_edges=confounders_edges,
            )

            for m in confounders_list:
                if m not in confounders:
                    confounders.append(m)

        return confounders_edges, confounders

    def request_confounders(self, treatment, outcome, analysis_context, domain_expertise, edited_factors_list,
                            temperature,
                            confounders_edges):
        confounders: List[str] = list()

        success: bool = False

        while not success:
            try:
                lm = self.llm
                with system():
                    lm += f"""You are an expert in {domain_expertise} and are studying {analysis_context}.
                    You are using your knowledge to help build a causal model that contains all the assumptions about {
                    analysis_context}. Where a causal model is a conceptual model that describes the causal 
                        mechanisms of a 
                            system. You
                    will do this by by answering questions about cause and effect and using your domain knowledge in 
    {domain_expertise}."""
                with user():
                    lm += f"""Follow the next two steps, and complete the first one before moving on to the second: (1) 
                                    From your perspective as an 
                    expert in {domain_expertise}, think step by step as you consider the factors that may interact 
                    between the {treatment} 
                    and the {outcome}. Use your knowlegde as an expert in {domain_expertise} to describe the 
                    confounders, 
                    if there are any 
                    at all, between the {treatment} and the {outcome}. Be concise and keep your thinking within two 
                    paragraphs. Then provide
                    your step by step chain of thoughts within the tags <thinking></thinking>. (2) From your 
                    perspective 
                    as an expert in 
                    {domain_expertise}, which factor(s) of the following factors, if any at all, has/have a high 
                    likelihood of directly 
                    influencing and causing both the assignment of the {treatment} and the {outcome}? Which factor(s) 
                    of 
                    the following 
                    factors, 
                    if any at all, have a causal chain that links to the {treatment} to the {outcome}? Which factor(
                    s) of 
                    the following 
                    factors, 
                    if any at all, are a confounder to the causal relationship between the {treatment} and the 
{outcome}? 
                    Be concise and 
                    keep your 
                    thinking within two paragraphs. Then provide your step by step chain of thoughts within the tags 
                    <thinking></thinking>. \n factor_names : 
                    {edited_factors_list} Wrap the name of the factor(s), if any at all, that has/have a high 
                    likelihood of 
                    directly influencing 
                    and causing both  the {treatment} and the {outcome}, within the tags 
                    <confounding_factor>factor_name</confounding_factor> where 
                    factor_name is one of the items within the factor_names list. If a factor does not have a high 
                    likelihood of directly 
                    confounding, then do not wrap the factor with any tags."""
                with system():
                    gen("output", temperature)

                output = lm["output"]
                confounding_factors = re.findall(r"<confounding_factor>(.*?)</confounding_factor>", output)

                if confounding_factors:
                    for factor in confounding_factors:
                        # to not add it twice into the list
                        if factor in edited_factors_list and factor not in confounders:
                            confounders.append(factor)
                    success = True
                else:
                    success = False

            except KeyError:
                success = False
                continue

        for element in confounders:
            if (element, treatment) in confounders_edges and (
                    element,
                    outcome,
            ) in confounders_edges:
                confounders_edges[(element, treatment)] += 1
                confounders_edges[(element, outcome)] += 1
            else:
                confounders_edges[(element, treatment)] = 1
                confounders_edges[(element, outcome)] = 1

        return confounders_edges, confounders

    # for the node factor, we want to find all the factors that can influence
    # this factor
    # if these influencing_factors exists, they are parents of the factor
    def suggest_parents(
<<<<<<< Updated upstream:pywhyllm/model_suggester.py
        self,
        analysis_context,
        factor,
        factors_list,
        expert,
        llm: guidance.llms,
        temperature=0.3,
        model_type=ModelType.Completion,
=======
            self,
            analysis_context,
            domain_expertise,
            factor,
            factors_list,
            temperature=0.3,
            model_type=ModelType.Completion,
>>>>>>> Stashed changes:pywhyllm/suggesters/model_suggester.py
    ):
        candidate_parent_list: List[str] = []

        for i in range(len(factors_list)):
            # another bug
            if factors_list[i] != factor:
                candidate_parent_list.append(factors_list[i])

        parents: List[str] = list()

        success: bool = False

        while not success:
            try:
                lm = self.llm
                with system():
                    lm += f"""You are an expert in {domain_expertise} and are studying {analysis_context}"""

                with user():
                    lm += f"""You are using your knowledge to help build a causal model that 
                      contains all the assumptions about the factors that are directly influencing and causing the 
          {factor}. 
                      Where a 
                      causal model is a conceptual model that describes the causal mechanisms of a system. You will 
                      do 
                      this by by 
                      answering questions about cause and effect and using your domain knowledge as an expert in {
                    domain_expertise}. 
                      Follow the next two steps, and complete the first one before moving on to the second: (1) From 
                      your perspective 
                      as an expert in {domain_expertise} think step by step as you consider the relevant factor 
                      directly 
                      influencing 
                      and causing the {factor}. Be concise and keep your thinking within two paragraphs. Then provide 
                      your step by 
                      step chain of thoughts within the tags <thinking></thinking>. (2) From your perspective as an 
                      expert in {
                    domain_expertise} which of the following factors has a high likelihood of directly influencing and 
                  causing 
                      the 
                      {factor}? factors list: [{factors_list}] For any factors within the list with a high likelihood 
                      of directly 
                      influencing and causing the {factor} wrap the name of the factor with the tags 
                      <influencing_factor>factor_name</influencing_factor>. If a factor does not have a high 
                      likelihood 
                      of directly 
                      influencing and causing the {factor}, then do not wrap the factor with any tags. Your answer as 
                      an expert 
                      in {
                    domain_expertise}:"""

                with assistant():
                    lm += gen("output")

                output = lm["output"]

                # influencing_factors must be the parent
                # basically, if a factor is an influencing_factor of the candidate
                # factor, then it is a parent
                influencing_factors = re.findall(
                    r"<influencing_factor>(.*?)</influencing_factor",
                    output,
                )

                if influencing_factors:
                    for factor in influencing_factors:
                        if factor in candidate_parent_list and factor not in parents:
                            parents.append(factor)
                    success = True
                else:
                    success = False

            except KeyError:
                success = False
                continue

        return parents

    def suggest_children(
<<<<<<< Updated upstream:pywhyllm/model_suggester.py
        self,
        analysis_context,
        factor,
        factors_list,
        expert,
        llm: guidance.llms,
        temperature=0.3,
        model_type=ModelType.Completion,
=======
            self,
            analysis_context,
            factor,
            factors_list,
            domain_expertise,
            temperature=0.3,
            model_type=ModelType.Completion,
>>>>>>> Stashed changes:pywhyllm/suggesters/model_suggester.py
    ):
        edited_factors_list: List[str] = []

        for i in range(len(factors_list)):
            if factors_list[i] not in factor:
                edited_factors_list.append(factors_list[i])

        children: List[str] = list()

        success: bool = False

        while not success:
            try:
                lm = self.llm
                with system():
                    lm += f"""You are an expert in {domain_expertise} and are studying {analysis_context}"""
                with user():
                    lm += f"""You are using your knowledge to help build a causal model that 
            contains all the assumptions about the factors that are directly influencing and causing the {factor}. 
            Where a 
            causal model is a conceptual model that describes the causal mechanisms of a system. You will do this by by 
            answering questions about cause and effect and using your domain knowledge as an expert in {
                    domain_expertise}. 
            Follow the next two steps, and complete the first one before moving on to the second: (1) From your 
            perspective 
            as an expert in {domain_expertise} think step by step as you consider which factor(s), from the factors 
            list, 
            if any at all, is/are directly influenced and caused by the {factor}. Be concise and keep your thinking 
            within 
            two paragraphs. Then provide your step by step chain of thoughts within the tags <thinking></thinking>. (2) 
            From 
            your perspective as an expert in {domain_expertise}, which of the following factor(s) from the factors 
            list, 
            if any at all, has/have a high likelihood of being directly influenced and caused by the {factor}? What 
            factor(
            s) from the factors list, if any at all, is/are affected by the {factor}? factors list: [{factors_list}] 
            For 
            any factors within the list with a high likelihood of being directly influenced and caused by the {factor}, 
            wrap the name of the factor with the tags <influencing_factor>factor_name</influencing_factor>. If a factor 
            has a 
            high likelihood of being affected and influenced by the {factor}, then wrap the name of the factor with the 
            tags <influencing_factor>factor_name</influencing_factor>. Where factor_name is one of the items within the 
            factor_names list. If a factor does not have a high likelihood of directly influencing and causing the {
                    factor}, then do not wrap the factor with any tags. Your answer as an expert in 
{domain_expertise}:"""

                with assistant():
                    lm += gen("output", temperature)

                output = lm["output"]

                influencing_factors = re.findall(
                    r"<influenced_factor>(.*?)</influenced_factor>",
                    output,
                )

                if influencing_factors:
                    for factor in influencing_factors:
                        if factor in edited_factors_list and factor not in children:
                            children.append(factor)
                    success = True
                else:
                    success = False

            except KeyError:
                success = False
                continue

            return children

    def suggest_pairwise_relationship(
<<<<<<< Updated upstream:pywhyllm/model_suggester.py
        self,
        expert,
        factor_a: str,
        factor_b: str,
        llm: guidance.llms,
        temperature=0.3,
        analysis_context: str = CONTEXT,
        model_type=ModelType.Completion,
=======
            self,
            domain_expertise,
            factor_a: str,
            factor_b: str,
            temperature=0.3,
            analysis_context: str = CONTEXT,
            model_type=ModelType.Completion,
>>>>>>> Stashed changes:pywhyllm/suggesters/model_suggester.py
    ):
        success: bool = False

        while not success:
            try:
                lm = self.llm
                with system():
                    lm += f"""You are an expert in {domain_expertise} and are 
            studying {analysis_context}. You are using your knowledge to help build a causal model that contains 
            all the 
            assumptions about {analysis_context}. Where a causal model is a conceptual model that describes the 
            causal 
            mechanisms of a system. You will do this by by answering questions about cause and effect and using your 
            domain 
            knowledge as an expert in {domain_expertise}."""
                with user():
                    lm += f"""From your perspective as an expert in {domain_expertise}, which of the following is 
                    most likely true? (A) {factor_a} affects {factor_b}; {factor_a} has a high likelihood of directly 
                    influencing {factor_b}; and {factor_a} causes {factor_b}. (B) {factor_b} affects {factor_a}; 
{factor_b} has a high likelihood of directly influencing {factor_a}; and {factor_b} causes {factor_a}. (C) Neither A 
nor B; {factor_a} does not cause {factor_b}; and {factor_b} does not cause {factor_a}. Select the answer that you as 
an expert in {domain_expertise} believe has the likelihood of being true. Think step by step and provide your 
thoughts within the tags <thinking></thinking>. Then select that answer A, B, or C, that is causally correct. When 
you reach a conclusion, wrap your answer within the tags <answer></answer>. If you are done thinking, provide your 
answer wrapped within the tags <answer></answer>. e.g. <answer>A</answer>, <answer>B</answer>, or <answer>C</answer>. 
Your answer as an expert in {domain_expertise}:"""

                with assistant():
                    lm += gen("output", temperature)

                output = lm["output"]

                answer = re.findall(
                    r"<answer>(.*?)</answer>",
                    output
                )

                if answer:
                    if answer[0] == "A" or answer[0] == "(A)":
                        return (factor_a, factor_b)

                    elif answer[0] == "B" or answer[0] == "(B)":
                        return (factor_b, factor_a)

                    elif answer[0] == "C" or answer[0] == "(C)":
                        return None
                    else:
                        success = False

                else:
                    success = False

            except KeyError:
                success = False
                continue

    '''
        factory method where given the relationship_strategy, would invoke the LLM
        to suggest the relationship between factors provided in factors_list
        suggest_relationships is trying to create the causal graph
        this is discovery
        where you can discover using Parent edges, Child edges, etc.
        as enumerated by RelationshipStrategy
    '''

    def suggest_relationships(
<<<<<<< Updated upstream:pywhyllm/model_suggester.py
        self,
        treatment: str,
        outcome: str,
        factors_list: list(),
        llm: guidance.llms,
        experts: list() = EXPERTS,
        analysis_context: str = CONTEXT,
        stakeholders: list() = None,
        temperature=0.3,
        model_type: ModelType = ModelType.Completion,
        relationship_strategy: RelationshipStrategy = RelationshipStrategy.Parent,
=======
            self,
            treatment: str,
            outcome: str,
            factors_list: list(),
            experts: list() = EXPERTS,
            analysis_context: str = CONTEXT,
            stakeholders: list() = None,
            temperature=0.3,
            model_type: ModelType = ModelType.Completion,
            relationship_strategy: RelationshipStrategy = RelationshipStrategy.Parent,
>>>>>>> Stashed changes:pywhyllm/suggesters/model_suggester.py
    ):
        expert_list: List[str] = list()
        for elements in experts:
            expert_list.append(elements)
        if stakeholders is not None:
            for elements in stakeholders:
                expert_list.append(elements)

        if relationship_strategy == RelationshipStrategy.Parent:
            "loop asking parents program"

            parent_edges: Dict[Tuple[str, str], int] = dict()

            for factor in factors_list:
                if len(expert_list) > 1:
                    for expert in expert_list:
                        suggested_parents = self.suggest_parents(
                            analysis_context=analysis_context,
                            factor=factor,
                            factors_list=factors_list,  # this is dubious
                            expert=expert,
                            temperature=temperature,
                            model_type=model_type,
                        )
                        for suggested_parent in suggested_parents:
                            # for each parent,
                            # TODO: bug
                            # fix: if (suggested_parent, factor) in parent_edges:
                            if (suggested_parent, factor) in parent_edges and suggested_parent in factors_list:
                                parent_edges[(suggested_parent, factor)] += 1
                            else:
                                parent_edges[(suggested_parent, factor)] = 1
                else:
                    suggested_parents = self.suggest_parents(
                        analysis_context=analysis_context,
                        factor=factor,
                        factors_list=factors_list,
                        expert=expert_list[0],
                        temperature=temperature,
                        model_type=model_type,
                    )

                    for suggested_parent in suggested_parents:
                        if (suggested_parent, factor) in parent_edges:
                            parent_edges[(suggested_parent, factor)] += 1
                        else:
                            parent_edges[(suggested_parent, factor)] = 1

            return parent_edges

        elif relationship_strategy == RelationshipStrategy.Child:
            "loop asking children program"

            children_edges: Dict[Tuple[str, str], int] = dict()

            for factor in factors_list:
                if len(expert_list) > 1:
                    for expert in expert_list:
                        suggested_children = self.suggest_children(
                            analysis_context=analysis_context,
                            factor=factor,
                            factors_list=factors_list,
                            expert=expert,
                            temperature=temperature,
                            model_type=model_type,
                        )
                        for suggested_parent in suggested_children:
                            if (
                                    suggested_parent,
                                    factor,
                            ) in children_edges and suggested_parent in factors_list:
                                children_edges[(suggested_parent, factor)] += 1
                            else:
                                children_edges[(suggested_parent, factor)] = 1
                else:
                    suggested_children = self.suggest_parents(
                        analysis_context=analysis_context,
                        factor=factor,
                        factors_list=factors_list,
                        expert=expert_list[0],
                        temperature=temperature,
                        model_type=model_type,
                    )

                    for suggested_parent in suggested_children:
                        if (suggested_parent, factor) in children_edges:
                            children_edges[(suggested_parent, factor)] += 1
                        else:
                            children_edges[(suggested_parent, factor)] = 1

            return children_edges

        elif relationship_strategy == RelationshipStrategy.Pairwise:
            "loop through all pairs asking relationship for"

            pairwise_edges: Dict[Tuple[str, str], int] = dict()

            for factor_a in factors_list:
                for factor_b in factors_list:
                    if factor_a != factor_b:
                        if len(expert_list) > 1:
                            for expert in expert_list:
                                suggested_edge = self.suggest_pairwise_relationship(
                                    analysis_context=analysis_context,
                                    factor_a=factor_a,
                                    factor_b=factor_b,
                                    expert=expert,
                                    temperature=temperature,
                                    model_type=model_type,
                                )

                                if suggested_edge is not None:
                                    if suggested_edge in pairwise_edges:
                                        pairwise_edges[suggested_edge] += 1
                                    else:
                                        pairwise_edges[suggested_edge] = 1
                        else:
                            suggested_edge = self.suggest_pairwise_relationship(
                                analysis_context=analysis_context,
                                factor_a=factor_a,
                                factor_b=factor_b,
                                expert=expert_list[0],
                                temperature=temperature,
                                model_type=model_type,
                            )

                            if suggested_edge is not None:
                                if suggested_edge in pairwise_edges:
                                    pairwise_edges[suggested_edge] += 1
                                else:
                                    pairwise_edges[suggested_edge] = 1

            return pairwise_edges

        elif relationship_strategy == RelationshipStrategy.Confounder:
            "one call to confounder program"

            confounders_counter, confounders = self.suggest_confounders(
                analysis_context=analysis_context,
                treatment=treatment,
                outcome=outcome,
                factors_list=factors_list,
                experts=experts,
                stakeholders=stakeholders,
                temperature=temperature,
                model_type=model_type,
            )

            return confounders_counter, confounders
