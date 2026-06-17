import tensorflow as tf
from keras import layers, models  

(x_train, y_train), (x_test, y_test) = tf.keras.datasets.fashion_mnist.load_data()

x_train = x_train / 255.0
x_test = x_test / 255.0

class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

model = models.Sequential([
    layers.Flatten(input_shape=(28, 28)),
    layers.Dense(128, activation='relu'),    
    layers.Dropout(0.2),                     
    layers.Dense(10, activation='softmax')
])


model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

model.summary()

history = model.fit(x_train, y_train, epochs=5)

test_loss, test_acc = model.evaluate(x_test, y_test, verbose=2)
print(f"\nTest accuracy: {test_acc:.4f}")

# 加入类别名称的预测结果展示
predictions = model.predict(x_test[:5])
for i in range(5):
    pred_class = tf.argmax(predictions[i]).numpy()
    print(f"样本{i} 预测类别: {class_names[pred_class]}, 真实类别: {class_names[y_test[i]]}")