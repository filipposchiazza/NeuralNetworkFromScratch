
import numpy as np
from hypothesis import given
from hypothesis.strategies import data
import hypothesis.strategies as st
import shutil

from neuralnet import ann
from neuralnet import activation_functions as act
from neuralnet import loss_functions as lf


max_num_neurons = 20

##################################################################################################################################

#Test the costruction of the neural network (the function __init__)

@given(inp = st.integers(min_value=1, max_value=1e5),
       hidd = st.lists(st.integers(min_value=1, max_value=max_num_neurons), min_size=0, max_size=10),
       out = st.integers(min_value=1, max_value=50))
def test_num_layers(inp, hidd, out):
    "Test if the number of layers is the correct one, according to the inputs given to build the ann"
    network = ann.Ann(num_inputs=inp, num_hidden=hidd, num_outputs=out, activation_function=act.sigmoid, loss_function=lf.binary_cross_entropy, seed=1)
    assert network.layers.size == len([network.num_inputs]) + network.num_hidden.size + len([network.num_outputs])
 

@given(inp = st.integers(min_value=1, max_value=1e5),
       hidd = st.lists(st.integers(min_value=1, max_value=max_num_neurons), min_size=0, max_size=10),
       out = st.integers(min_value=1, max_value=50)) 
def test_num_weights(inp, hidd, out):
    "Test if the total number of weights of the neural network is the correct one, according to the inputs given to build it"
    network = ann.Ann(num_inputs=inp, num_hidden=hidd, num_outputs=out, activation_function=act.sigmoid, loss_function=lf.binary_cross_entropy, seed=1)
    counter_first = 0
    for i in range(len(network.layers)-1):
        counter_first += (network.layers[i]) * (network.layers[i+1])
    counter_second = 0
    for i in range(len(network.weights)):
        for j in range(len(network.weights[i])):
            counter_second += len(network.weights[i][j])
    assert counter_first == counter_second


@given(inp = st.integers(min_value=1, max_value=1e5),
       hidd = st.lists(st.integers(min_value=1, max_value=max_num_neurons), min_size=0, max_size=10),
       out = st.integers(min_value=1, max_value=50)) 
def test_num_biases(inp, hidd, out):
    "Test if the total number of biases is equal to (total number of neurons - number of neurons in the input layer)"
    network = ann.Ann(num_inputs=inp, num_hidden=hidd, num_outputs=out, activation_function=act.sigmoid, loss_function=lf.binary_cross_entropy, seed=1)
    counter_first = 0
    for b in network.biases:
        counter_first += b.size
    counter_second = 0
    for i in range(1, len(network.layers)):
        counter_second += network.layers[i]
    assert counter_first == counter_second


@given(inp = st.integers(min_value=1, max_value=1e5),
       hidd = st.lists(st.integers(min_value=1, max_value=max_num_neurons), min_size=0, max_size=10),
       out = st.integers(min_value=1, max_value=50))
def test_num_linear_comb(inp, hidd, out):
    "Test if the total number of linear combinations is equal to (total number of neurons - number of neurons in the input layer)"
    network = ann.Ann(num_inputs=inp, num_hidden=hidd, num_outputs=out, activation_function=act.sigmoid, loss_function=lf.binary_cross_entropy, seed=1)
    counter_first = 0
    for lin in network.linear_comb:
        counter_first += lin.size
    counter_second = 0
    for i in range(1, len(network.layers)):
        counter_second += network.layers[i]
    assert counter_first == counter_second
    
    
@given(inp = st.integers(min_value=1, max_value=1e5),
       hidd = st.lists(st.integers(min_value=1, max_value=max_num_neurons), min_size=0, max_size=10),
       out = st.integers(min_value=1, max_value=50))
def test_num_activations(inp, hidd, out):
    "Test if the numbers of activations stored for each layer is the correct one (corresponding to the number of neurons)"
    network = ann.Ann(num_inputs=inp, num_hidden=hidd, num_outputs=out, activation_function=act.sigmoid, loss_function=lf.binary_cross_entropy, seed=1)
    for i in range(len(network.layers)):
        assert len(network.activations[i]) == network.layers[i] 

        
@given(inp = st.integers(min_value=1, max_value=1e5),
       hidd = st.lists(st.integers(min_value=1, max_value=max_num_neurons), min_size=0, max_size=10),
       out = st.integers(min_value=1, max_value=50))
def test_num_weights_derivatives(inp, hidd, out):
    "Test if the number of weights'derivatives stored is the same of the number of weights (as it should be)"
    network = ann.Ann(num_inputs=inp, num_hidden=hidd, num_outputs=out, activation_function=act.sigmoid, loss_function=lf.binary_cross_entropy, seed=1)
    for i in range(len(network.weights)):
        assert network.weights[i].size == network.weights_deriv[i].size


@given(inp = st.integers(min_value=1, max_value=1e5),
       hidd = st.lists(st.integers(min_value=1, max_value=max_num_neurons), min_size=0, max_size=10),
       out = st.integers(min_value=1, max_value=50)) 
def test_num_biases_derivatives(inp, hidd, out):
    "Test if the number of biases'derivatives stored is the same of the number of weights (as it should be)"
    network = ann.Ann(num_inputs=inp, num_hidden=hidd, num_outputs=out, activation_function=act.sigmoid, loss_function=lf.binary_cross_entropy, seed=1)
    for i in range(len(network.biases)):
        assert network.biases[i].size == network.biases_deriv[i].size

##########################################################################################################################

# Test the forward propagation method

def test_specific_case_forward_propagation():
    "Test the output of the forward propagation for a specific combination of inputs, weights and biases"
    w1 = np.array([[0.5, 0.4], [0.3, 0.7]])
    b1 = np.array([0.3, 0.6])
    weights = [w1]
    biases = [b1]
    neural_network = ann.Ann(num_inputs = 2, num_hidden = [], num_outputs = 2,
                             activation_function = act.softmax, 
                             loss_function = lf.cross_entropy,
                             seed=1)
    neural_network._set_parameters(weights, biases)
    inputs = [1., 1.]
    result = neural_network._forward_prop(inputs)
    expected_result = np.array([0.35434369, 0.64565631])
    assert np.all(np.isclose(result, expected_result, rtol=0.1, atol=1e-5))
    
    
def test_limit_case_forward_propagation():
    "Test the output of the forward propagation for the limit case when all the weights and biases are equal to 0"
    w1 = np.array([[0., 0.], [0., 0.]])
    b1 = np.array([0.0, 0.0])
    w2 = np.array([[0.], [0.]])
    b2 = np.array([0.])
    weights = [w1, w2]
    biases = [b1, b2]
    neural_network = ann.Ann(num_inputs = 2, num_hidden = [2], num_outputs = 1,
                             activation_function = act.sigmoid, 
                             loss_function = lf.binary_cross_entropy,
                             seed=1)
    neural_network._set_parameters(weights, biases)
    inputs = [1., 1.]
    result = neural_network._forward_prop(inputs)
    expected_result = np.array([0.5])
    assert np.all(np.isclose(result, expected_result, rtol=0.1, atol=1e-5))
    
    
@given(inp = st.integers(min_value=1, max_value=1e5),
       hidd = st.lists(st.integers(min_value=1, max_value=max_num_neurons), min_size=0, max_size=10),
       out = st.integers(min_value=1, max_value=50))
def test_forward_prop(inp, hidd, out):
    "Test that the dimension of the forward propagation result is the same as the number of output layers of the neural network"
    np.random.seed(1)
    dataset = np.random.randn(inp)
    network = ann.Ann(num_inputs=inp, num_hidden=hidd, num_outputs=out, activation_function=act.sigmoid, loss_function=lf.binary_cross_entropy, seed=1)
    assert network.num_outputs == network._forward_prop(inputs=dataset).size
    
########################################################################################################################## 

# Test the backward propagation method

def test_specific_case_backward_propagation():
    "Test the output of the backward propagation for a specific combination of error, weights and biases"
    w1 = np.array([[0.5, 0.4], [0.3, 0.7]])
    b1 = np.array([0.2, 0.1])
    w2 = np.array([[0.1], [0.2]])
    b2 = np.array([0.01])
    weights = [w1, w2]
    biases = [b1, b2]
    neural_network = ann.Ann(num_inputs = 2, num_hidden = [2], num_outputs = 1,
                             activation_function = act.sigmoid, 
                             loss_function = lf.binary_cross_entropy,
                             seed=1)
    neural_network._set_parameters(weights, biases)
    error = [1.]
    result = neural_network._backward_prop(error)
    expected_result = np.array([0.008125, 0.010625])
    assert np.all(np.isclose(result, expected_result, rtol=0.1, atol=1e-5))
    
    
def test_limit_case_backward_propagation():
    "Test the output of the backward propagation for the limit case when all the weights and biases are equal to 0"
    w1 = np.array([[0., 0.], [0., 0.]])
    b1 = np.array([0., 0.])
    w2 = np.array([[0.], [0.]])
    b2 = np.array([0.])
    weights = [w1, w2]
    biases = [b1, b2]
    neural_network = ann.Ann(num_inputs = 2, num_hidden = [2], num_outputs = 1,
                         activation_function = act.sigmoid, 
                         loss_function = lf.binary_cross_entropy,
                         seed=1)
    neural_network._set_parameters(weights, biases)
    error = [1.]
    result = neural_network._backward_prop(error)
    expected_result = np.array([0., 0.])
    assert np.all(np.isclose(result, expected_result, rtol=0.1, atol=1e-5))


@given(inp = st.integers(min_value=1, max_value=1e5),
       hidd = st.lists(st.integers(min_value=1, max_value=max_num_neurons), min_size=0, max_size=10),
       out = st.integers(min_value=1, max_value=20))
def test_weights_deriv_after_backprop(inp, hidd, out):
    "Test that, after backpropagation, the dimensionalities of the weights'derivatives is still the same as the ones of weights"
    network = ann.Ann(num_inputs=inp, num_hidden=hidd, num_outputs=out, 
                      activation_function=act.sigmoid, 
                      loss_function=lf.binary_cross_entropy,
                      seed=1)
    np.random.seed(1)
    error = np.random.uniform(-100, 100, out)
    network._backward_prop(error=error)
    for i in range(len(network.weights)):
        for j in range(len(network.weights[i])):
            assert network.weights_deriv[i][j].size == network.weights[i][j].size
   
@given(inp = st.integers(min_value=1, max_value=1e5),
       hidd = st.lists(st.integers(min_value=1, max_value=max_num_neurons), min_size=0, max_size=10),
       out = st.integers(min_value=1, max_value=50))
def test_biases_deriv_after_backprop(inp, hidd, out):
    "Test that, after backpropagation, the dimensionalities of the biases'derivatives is still the same as the ones of biases"
    network = ann.Ann(num_inputs=inp, num_hidden=hidd, num_outputs=out, 
                      activation_function=act.sigmoid, 
                      loss_function=lf.binary_cross_entropy,
                      seed=1)
    error = np.linspace(-100, 100, out)
    network._backward_prop(error=error)
    for i in range(len(network.biases)):
        assert network.biases_deriv[i].size == network.biases[i].size    


##########################################################################################################################

# Test the gradient descendent method

def test_specific_case_gradient_descendent():
    neural_network = ann.Ann(num_inputs = 2, num_hidden = [], num_outputs = 2, 
                             activation_function = act.sigmoid,
                             loss_function = lf.binary_cross_entropy,
                             seed=1)
    neural_network.weights = [np.array([[0.5, 0.4], [0.7, 0.5]])]
    neural_network.biases = [np.array([0.6, 0.4])]
    neural_network.weights_deriv = [np.array([[0.5, 0.4], [0.7, 0.5]])]
    neural_network.biases_deriv = [np.array([0.6, 0.4])]
    neural_network._gradient_descendent(learning_rate=1)
    expected_weights = [np.array([[0., 0.], [0., 0.]])]
    expected_biases = [np.array([0., 0.])]
    assert np.all(np.isclose(neural_network.weights[0], expected_weights, rtol=0.1, atol=1e-5))
    assert np.all(np.isclose(neural_network.biases[0], expected_biases, rtol=0.1, atol=1e-5))


def test_limit_case_gradient_descendent():
    "Test the specific case when all the weights and biases' derivatives are equal to zero, so no update of weights and biases is expected"
    neural_network = ann.Ann(num_inputs = 2, num_hidden = [2], num_outputs = 1,
                         activation_function = act.sigmoid, 
                         loss_function = lf.binary_cross_entropy,
                         seed=1)
    weights_before = [np.copy(neural_network.weights[0]), np.copy(neural_network.weights[1])]
    biases_before = [np.copy(neural_network.biases[0]), np.copy(neural_network.biases[1])]
    neural_network.biases_deriv = [np.array([0., 0.]), np.array([0.])]
    neural_network.weights_deriv = [np.array([[0. , 0.], [0., 0.]]), np.array([[0.], [0.]])]
    neural_network._gradient_descendent(learning_rate=0.5)
    assert np.all(np.isclose(neural_network.weights[0], weights_before[0], rtol=0.1, atol=1e-5))
    assert np.all(np.isclose(neural_network.weights[1], weights_before[1], rtol=0.1, atol=1e-5))
    assert np.all(np.isclose(neural_network.biases[0], biases_before[0], rtol=0.1, atol=1e-5))
    assert np.all(np.isclose(neural_network.biases[1], biases_before[1], rtol=0.1, atol=1e-5))


@given(inp = st.integers(min_value=1, max_value=1e5),
       hidd = st.lists(st.integers(min_value=1, max_value=max_num_neurons), min_size=0, max_size=10),
       out = st.integers(min_value=1, max_value=50),
       learning_rate = st.floats(min_value=0.0001, max_value=10, allow_nan=False))
def test_weights_structure_after_gradient (inp, hidd, out, learning_rate):
    "Test that the dimensionalities of the weights is still the same after the gradient descendent"
    network = ann.Ann(num_inputs=inp, num_hidden=hidd, num_outputs=out, 
                      activation_function=act.sigmoid, 
                      loss_function=lf.binary_cross_entropy,
                      seed=1)
    error = np.linspace(-100, 100, out)
    network._backward_prop(error=error)
    
    previous_weights = []
    for i in range(len(network.layers) - 1):
        previous_weights.append(np.copy(network.weights[i]))
    
    network._gradient_descendent(learning_rate=learning_rate)
    
    for i in range(len(network.weights)):
        for j in range(len(network.weights[i])):
            assert network.weights[i][j].size == previous_weights[i][j].size
            
            
@given(inp = st.integers(min_value=1, max_value=1e5),
       hidd = st.lists(st.integers(min_value=1, max_value=max_num_neurons), min_size=0, max_size=10),
       out = st.integers(min_value=1, max_value=50),
       learning_rate = st.floats(min_value=0.0001, max_value=10, allow_nan=False))
def test_biases_structure_after_gradient (inp, hidd, out, learning_rate):
    "Test if the dimensionalities of the biases is still the same after the gradient descendent"
    network = ann.Ann(num_inputs=inp, num_hidden=hidd, num_outputs=out, 
                      activation_function=act.sigmoid, 
                      loss_function=lf.binary_cross_entropy,
                      seed=1)
    error = np.linspace(-100, 100, out)
    network._backward_prop(error=error)
    
    previous_biases = []
    for i in range(len(network.layers) - 1):
        previous_biases.append(np.copy(network.biases[i]))
    
    network._gradient_descendent(learning_rate=learning_rate)
    
    for i in range(len(network.biases)):
        assert network.biases[i].size == previous_biases[i].size
      
 
##########################################################################################################################

# Test the train method  -> not necessary because it is the collection of methods already tested.

##########################################################################################################################

# Test the predict method

def test_predict_for_binary_classification_specific():
    "Test the prediction method in the case of binary classification with specific inputs (all equal to 1), biases and weights"
    # set weights' values
    w1 = np.array([[0.5, 0.4], [0.3, 0.7]])
    w2 = np.array([[0.1], [0.2]])
    # set biases' values
    b1 = np.array([0.2, 0.1])
    b2 = np.array([0.01])
    weights = [w1, w2]
    biases = [b1, b2]
    neural_network = ann.Ann(num_inputs = 2, num_hidden = [2], num_outputs = 1,
                             activation_function = act.sigmoid, 
                             loss_function = lf.binary_cross_entropy,
                             seed=1)
    neural_network._set_parameters(weights, biases)
    inputs = np.ones((5,2))
    result = neural_network.predict(inputs)
    expected_result = np.array([[0.55892758], [0.55892758], [0.55892758], [0.55892758], [0.55892758]])
    assert np.all(np.isclose(result, expected_result, rtol=0.1, atol=1e-5))
    
    
def test_predicti_for_multiclass_classification_specific():
    "Test the prediction method in the case of multi-class classification with specific inputs, biases and weights"
    # set weights' values
    w1 = np.array([[0.5, 0.7], [0.4, 0.6]])
    w2 = np.array([[0.1, 0.5], [0.9, 0.2]])
    weights = [w1, w2]
    # set biases's values
    b1 = np.array([0.02, 0.7])
    b2 = np.array([0.3, 0.1])
    biases = [b1, b2]
    neural_network = ann.Ann(num_inputs = 2, num_hidden = [2], num_outputs = 2,
                             activation_function = act.softmax, 
                             loss_function = lf.cross_entropy,
                             seed=1)
    neural_network._set_parameters(weights, biases)
    inputs = np.array([[1, 1], [0.2, 0.2]])
    result = neural_network.predict(inputs)
    expected_result = np.array([[0.6500892, 0.3499108], [0.63453863, 0.36546137]])
    assert np.all(np.isclose(result, expected_result, rtol=0.1, atol=1e-5))
    
    
@given(inp = st.integers(min_value=1, max_value=1e5),
       hidd = st.lists(st.integers(min_value=1, max_value=max_num_neurons), min_size=0, max_size=10),
       len_dataset = st.integers(min_value=1, max_value=100))
def test_range_predictions_binary_classification(inp, hidd, len_dataset):
    "Test that all the predictions in the case of binary classification are in the expected range [0, 1]"
    neural_network = ann.Ann(num_inputs = inp, num_hidden = hidd, num_outputs = 1,
                             activation_function = act.sigmoid, 
                             loss_function = lf.binary_cross_entropy,
                             seed=1)
    # create a toy dataset
    inputs = np.linspace(start = -2, stop = 2, num = inp*len_dataset)
    inputs = inputs.reshape((len_dataset, inp))
    predictions = neural_network.predict(inputs = inputs)
    assert np.all(predictions<=1) and np.all(predictions>=0)
    

@given(inp = st.integers(min_value=1, max_value=1e5),
       hidd = st.lists(st.integers(min_value=1, max_value=max_num_neurons), min_size=0, max_size=3),
       out = st.integers(min_value=1, max_value=10),
       len_dataset = st.integers(min_value=1, max_value=30))
def test_range_predictions_multiclass_classification(inp, hidd, out, len_dataset):
    "Test that all the predictions in the case of multi-class classification are in the expected range [0, 1]"
    neural_network = ann.Ann(num_inputs = inp, num_hidden = hidd, num_outputs = out,
                             activation_function = act.softmax, 
                             loss_function = lf.cross_entropy,
                             seed=1)
    # create a toy dataset
    inputs = np.linspace(start = -2, stop = 2, num = inp*len_dataset)
    inputs = inputs.reshape((len_dataset, inp))
    predictions = neural_network.predict(inputs = inputs)
    assert np.all(predictions<=1) and np.all(predictions>=0)
    
########################################################################################################################## 

# Test discretization method

def test_specific_case_discretization_binary_classification():
    "Test that all the element of the discretization output are eighter 1 or 0, in the case of binary classification"
    neural_network = ann.Ann(num_inputs = 3, num_hidden = [2], num_outputs = 1, 
                             activation_function = act.sigmoid,
                             loss_function = lf.binary_cross_entropy,
                             seed=1)
    predictions = np.array([0.3, 0.5, 0.8])
    pred_discr = neural_network._discretize_predictions(predictions)
    s1 = pred_discr==1
    s2 = pred_discr==0
    assert np.all(s1+s2)
  
    
def test_single_discretization_prediction():
    "Test discretization output when there is only one input"
    neural_network = ann.Ann(num_inputs = 3, num_hidden = [2], num_outputs = 1, 
                             activation_function = act.sigmoid,
                             loss_function = lf.binary_cross_entropy,
                             seed=1)
    predictions = np.array([0.3])
    pred_discr = neural_network._discretize_predictions(predictions)
    assert pred_discr==1 or pred_discr==0


def test_specific_case_discretization_multiclass_classification():
    "Test that all the element of the discretization output are eighter 1 or 0, in the case of multi-class classification"
    neural_network = ann.Ann(num_inputs = 3, num_hidden = [2], num_outputs = 2, 
                             activation_function = act.softmax,
                             loss_function = lf.cross_entropy,
                             seed=1)
    predictions = np.array([[0.8, 0.2], [0.75, 0.25], [0.45, 0.65], [0.1, 0.9]])
    pred_discr = neural_network._discretize_predictions(predictions)
    s1 = pred_discr==1
    s2 = pred_discr==0
    assert np.all(s1+s2)
    

@given(predictions = st.lists(st.floats(min_value=0., max_value=1.), min_size=1, max_size=100))
def test_discretization_bynary_class(predictions):
    "Test that all the element of the discretization output are eighter 1 or 0, in the case of binary classification"
    neural_network = ann.Ann(num_inputs = 3, num_hidden = [2], num_outputs = 1, 
                             activation_function = act.softmax,
                             loss_function = lf.cross_entropy,
                             seed=1)
    predictions = np.array(predictions)
    pred_discr = neural_network._discretize_predictions(predictions)
    s1 = pred_discr==1
    s2 = pred_discr==0
    assert np.all(s1+s2)


@given(predictions = st.lists(st.lists(st.floats(min_value=0., max_value=1.), min_size=3, max_size=3), min_size=1, max_size=100))
def test_discretization_multiclass(predictions):
    "Test that all the element of the discretization output are eighter 1 or 0, in the case of multi-class classification"
    neural_network = ann.Ann(num_inputs = 3, num_hidden = [2], num_outputs = len(predictions), 
                             activation_function = act.softmax,
                             loss_function = lf.cross_entropy,
                             seed=1)
    predictions = np.array(predictions)
    pred_discr = neural_network._discretize_predictions(predictions)
    s1 = pred_discr==1
    s2 = pred_discr==0
    assert np.all(s1+s2)

##########################################################################################################################


# Test the evaluate classification method

target_values = [0., 1.]

@given(inp = st.integers(min_value=1, max_value=1e5),
       hidd = st.lists(st.integers(min_value=1, max_value=max_num_neurons), min_size=0, max_size=3),
       out = st.integers(min_value=1, max_value=10),
       len_dataset = st.integers(min_value=1, max_value=30),
       data = data())
def test_number_correct_prediction_is_in_meaningful_range(inp, hidd, out, len_dataset, data):
    "Test that the number of correct predictions is in the range between 0 and the total number of predictions"
    if out == 1:
        ann_test = ann.Ann(num_inputs=inp, num_hidden=hidd, num_outputs=out, 
                           activation_function=act.sigmoid, 
                           loss_function=lf.binary_cross_entropy,
                           seed=1)
    else:
        ann_test = ann.Ann(num_inputs=inp, num_hidden=hidd, num_outputs=out, 
                           activation_function=act.softmax, 
                           loss_function=lf.cross_entropy,
                           seed=1)
    
    targets = np.zeros((len_dataset, out))
    for i in range(len(targets)):
       targets[i] = data.draw(st.lists(st.sampled_from(target_values), min_size=out, max_size=out))
    targets = np.array(targets)
    inputs = np.linspace(start = -2, stop = 2, num = inp*len_dataset)
    inputs = inputs.reshape((len_dataset, inp))   
    a, num_correct_classification, c = ann_test.evaluate_classification(inputs=inputs, targets=targets) 
    assert num_correct_classification >= 0 and num_correct_classification <= len(targets)


##########################################################################################################################

# Test saving and loading methods

def test_save_and_load():
    "Test that saving and loading method correctly save and load the neural network"
    neural_network = ann.Ann(num_inputs = 5, num_hidden = [4, 3], num_outputs = 2, 
                             activation_function = act.softmax, 
                             loss_function = lf.cross_entropy,
                             seed=1)
    # save the neural network
    location = 'saving_test/'
    neural_network.save(directory_name = location)
    neural_network_loaded = ann.Ann.load_neural_network(directory_name = location)
    
    # remove the directory
    shutil.rmtree(location)
    
    assert neural_network_loaded.activation_func == neural_network.activation_func
    assert neural_network_loaded.loss_func == neural_network.loss_func
    assert neural_network_loaded.num_inputs == neural_network.num_inputs
    assert np.all(neural_network_loaded.num_hidden == neural_network.num_hidden)
    assert neural_network_loaded.num_outputs == neural_network.num_outputs
    for i in range(len(neural_network.layers) - 1):
        assert np.all(neural_network_loaded.biases[i] == neural_network.biases[i])
    for i in range(len(neural_network.layers) - 1):
        assert np.all(neural_network_loaded.weights[i] == neural_network.weights[i])
        
