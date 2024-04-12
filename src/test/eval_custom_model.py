# import functions
from deepeval.models.base_model import DeepEvalBaseLLM
from deepeval.metrics import AnswerRelevancyMetric, FaithfulnessMetric, ContextualRelevancyMetric, HallucinationMetric, BiasMetric, ToxicityMetric
from deepeval.test_case import LLMTestCase

class LLM(DeepEvalBaseLLM):
    def __init__(
        self,
        model,
        model_name
    ):
        self.model = model
        self.model_name = model_name

    def load_model(self):
        return self.model

    def generate(self, prompt: str) -> str:
        model = self.load_model()
        return model(prompt)

    async def a_generate(self, prompt: str) -> str:
        return self.generate(prompt)

    def get_model_name(self):
        return self.model_name
    
def eval_answer_relevancy_metric(llm: LLM, question: str, answer: str, context: list):
    answer_relevancy_metric = AnswerRelevancyMetric(model=llm, threshold=0.5, include_reason=True)
    test_case = LLMTestCase(
        input=question,
        actual_output=answer,
        retrieval_context=context
    )

    answer_relevancy_metric.measure(test_case)
    return answer_relevancy_metric.score

def eval_faithfulness_metric(llm: LLM, question: str, answer: str, context: list):
    faithfulness_metric = FaithfulnessMetric(model=llm, threshold=0.5, include_reason=True)
    test_case = LLMTestCase(
        input=question,
        actual_output=answer,
        retrieval_context=context
    )

    faithfulness_metric.measure(test_case)
    return faithfulness_metric.score

def eval_contextual_relevancy_metric(llm: LLM, question: str, answer: str, context: list):
    contextual_relevancy_metric = ContextualRelevancyMetric(model=llm, threshold=0.5, include_reason=False)
    test_case = LLMTestCase(
        input=question,
        actual_output=answer,
        retrieval_context=context
    )

    contextual_relevancy_metric.measure(test_case)
    return contextual_relevancy_metric.score

def eval_hallucination_metric(llm: LLM, question: str, answer: str, context: list):
    hallucination_metric = HallucinationMetric(model=llm, threshold=0.5, include_reason=True)
    test_case = LLMTestCase(
        input=question,
        actual_output=answer,
        context=context
    )

    hallucination_metric.measure(test_case)
    return hallucination_metric.score

def eval_bias_metric(llm: LLM, question: str, answer: str):
    bias_metric = BiasMetric(model=llm, threshold=0.5, include_reason=True)
    test_case = LLMTestCase(
        input=question,
        actual_output=answer
    )

    bias_metric.measure(test_case)
    return bias_metric.score

def eval_toxicity_metric(llm: LLM, question: str, answer: str):
    toxicity_metric = ToxicityMetric(model=llm, threshold=0.5, include_reason=True)
    test_case = LLMTestCase(
        input=question,
        actual_output=answer
    )

    toxicity_metric.measure(test_case)
    return toxicity_metric.score

def eval_rag_metrics(llm: LLM, question: str, answer: str, context: list) -> dict:
    return {
            "AnswerRelevancyMetric": eval_answer_relevancy_metric(llm, question, answer, context),
            "FaithfulnessMetric": eval_faithfulness_metric(llm, question, answer, context),
            "ContextualRelevancyMetric": eval_contextual_relevancy_metric(llm, question, answer, context),
            # "HallucinationMetric": eval_hallucination_metric(llm, question, answer, context),
            # "BiasMetric": eval_bias_metric(llm, question, answer),
            # "ToxicityMetric": eval_toxicity_metric(llm, question, answer),
        }