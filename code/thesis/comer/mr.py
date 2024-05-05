class MetamorphicRelation:
    def __init__(self, input_variable, output_variable, transformation_rule):
        self.input_variable = input_variable
        self.output_variable = output_variable
        self.transformation_rule = transformation_rule

    def apply(self, test_case):
        # Apply the transformation rule to the input variables
        transformed_input = [self.transformation_rule(x) for x in test_case[self.input_variable]]
        return {**test_case, **{self.output_variable: transformed_input}}
