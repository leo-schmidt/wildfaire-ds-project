import tensorflow as tf

def custom_loss(class_weights):
    def loss(y_true, y_pred):
        weighted_loss = tf.nn.weighted_cross_entropy_with_logits(
            y_true, y_pred, class_weights)
        return tf.reduce_mean(weighted_loss)
    return loss

def loss(y_true, y_pred):
        weighted_loss = tf.nn.weighted_cross_entropy_with_logits(
            y_true, y_pred, class_weights)
        return tf.reduce_mean(weighted_loss)
