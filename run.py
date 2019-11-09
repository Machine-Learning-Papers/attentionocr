import string

from attentionocr import VectorizerOCR, AttentionOCR, FlatDirectoryIterator
from attentionocr.vectorizer import VectorizedBatchGenerator

if __name__ == "__main__":
    vocabulary = list(string.ascii_lowercase) + list(string.digits)
    vec = VectorizerOCR(vocabulary=vocabulary, image_width=320)
    model = AttentionOCR(vectorizer=vec)
    train_data = list(FlatDirectoryIterator('train/*.jpg'))
    test_data = list(FlatDirectoryIterator('test/*.jpg'))

    # images, texts = zip(*train_data)
    # model.fit(images=images, texts=texts, epochs=1, batch_size=64)

    generator = VectorizedBatchGenerator(vectorizer=vec)
    train_bgen = generator.flow_from_dataset(train_data)
    test_bgen = generator.flow_from_dataset(test_data)
    model.fit_generator(train_bgen, epochs=20, steps_per_epoch=100, validation_data=test_bgen)

    for i in range(10):
        filename, text = test_data[i]
        image = vec.load_image(filename)
        pred = model.predict([image])[0]
        print('Input:', text, " prediction: ", pred)
