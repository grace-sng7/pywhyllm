TEST_VARIABLE_LISTS = {
    "list1": ["temperature", "ice cream sales", "cavities"],
    "list1_expected_domain_expertises": ['Econometrics/Behavioral Economics'],
    "list1_expected_domain_experts": ['Climate Scientist or Meteorologist',
                                      'Dentist or Oral Health Expert',
                                      'Marketing Analyst',
                                      'Nutrition Scientist or Dietician',
                                      'Statistician or Data Scientist'],
    "list1_expected_stakeholders": ['Climate Scientists',
                                    'Ice cream Manufacturers or Sellers',
                                    'Dentists or Dental Researchers',
                                    'Consumer Behavior Analysts',
                                    'Nutritionists or Dieticians'],
    "list1_expected_parents": ['temperature'],
    "list1_expected_children": ['cavities']
}

TEST_PAIRS = {
    "test_a_cause_b": ["temperature", "ice cream sales"],
    "test_a_cause_b_expected_result": ("temperature", "ice cream sales", "The answer is <answer>A</answer>."),
    "test_b_cause_a": ["temperature", "ice cream sales"],
    "test_b_cause_a_expected_result": ("ice cream sales", "temperature", "The answer is <answer>B</answer>."),
    "test_no_causality": ["temperature", "ice cream sales"],
    "test_no_causality_expected_result": (None, None, "The answer is <answer>C</answer>."),
}
