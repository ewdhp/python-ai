"""
Bayesian Networks:

Focus: A Bayesian Network represents probabilistic dependencies among a set of variables. 
The key difference is that Bayesian Networks allow for conditional dependencies between 
multiple variables, not just between sequential states.

Structure: It uses a directed acyclic graph (DAG) where each node represents a variable, 
and edges represent dependencies (i.e., the probability of one variable is conditional on 
others).

Example: Consider a system where:

A (Rain), B (Wet road), and C (Umbrella) are related.
A influences both B and C, but B and C may not directly affect each other.

Key Differences:

- Markov Chains are generally used for sequential processes, where you have a series 
of states, and the system evolves over time based on the current state.

- Bayesian Networks are more general and flexible, capable of modeling complex 
  probabilistic relationships with multiple variables, not just sequential dependencies.

In summary:
Markov Chains focus on modeling the transition between states over time based on current 
knowledge.
Bayesian Networks represent joint probabilities among variables and allow for a richer 
set of conditional dependencies between them, but they don't require the sequential 
structure that Markov Chains rely on.
"""
from pgmpy.models import BayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination

# Create the Bayesian Network structure
model = BayesianNetwork([('A', 'B'), ('A', 'C')])

# Define the conditional probability distributions (CPDs)
cpd_A = TabularCPD(variable='A', variable_card=2, values=[[0.7], [0.3]])  # 70% chance it's not raining, 30% it's raining
cpd_B = TabularCPD(variable='B', variable_card=2, 
                   values=[[0.9, 0.2], [0.1, 0.8]],  # P(B|A)
                   evidence=['A'], evidence_card=[2])
cpd_C = TabularCPD(variable='C', variable_card=2, 
                   values=[[0.5, 0.1], [0.5, 0.9]],  # P(C|A)
                   evidence=['A'], evidence_card=[2])

# Add CPDs to the model
model.add_cpds(cpd_A, cpd_B, cpd_C)

# Check if the model is valid
assert model.check_model()

# Perform inference
inference = VariableElimination(model)

# Query the probability of C given that B is true (i.e., the road is wet)
prob_C_given_B = inference.query(variables=['C'], evidence={'B': 1})
print(prob_C_given_B)
