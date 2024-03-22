# Content Based Recommendation System – Using Image classification and Text Generation
The aim of this project is to provide product recommendation based on title text, description text
and images. There are three approaches for this project:

- Text Based Product Recommendation which will use Bag of words, Term Frequency
Inverse Document Frequency (TF-IDF), Word2Vec.
- Image Based Product Recommendation: For this recommendation system, you can train the following state of the art models like VGG, Resnet, FashionNet, Inception etc ( at least
2 ) and compare the results.
- Image – Text Recommendation System: For this system use Natural Language Processing techniques to understand textual queries or descriptions provided by users and then recommend relevant accordingly. You can use pre-trained models like BERT, GPT, Transformer etc.
## Goal
Develop a recommendation system capable of accepting user input in the form of images, product titles, and descriptions, and provide personalized recommendations based on the content of the images as well as the textual information such as titles and descriptions of products.
## Dataset
You can use any one of the datasets or more if you want to compare the results from each dataset.
Please note it takes time to extract the features for Image Classification, you either reduce the
size of the dataset or train it on google collab and save the features to reload for future use.
1. Amazon Apparel (Woman’s Tops) Dataset. (Dataset scraped from Amazon Website)
28k_apparel_data.csv
The dataset contains six features:
1. Asin (Amazon Standard Identification Number)
2. Brand ( to which brand the product belongs to)
3. Color ( color information of apparel, it can contain many colours as a value of ex: red and
black stripes)
4. Product_type_name ( type of the apparel, ex: SHIRT/TSHIRT)
5. Medium_image_url ( url of the image)
6. Title ( title of the product)
7. Formatted_price ( price of the product)
Note: To extract the image from feature column “medium_image_url”, use Python Imaging
Library and save it in a file .
2. Polyvore Outfit Dataset Link: https://github.com/xthan/polyvore-dataset
3. Fashion200k Dataset Link : https://github.com/ecom-research/ComposeAE
4. DeepFashion Dataset Link : https://liuziwei7.github.io/projects/DeepFashion.html
Evaluation Metrics:
- Compatibility Prediction
- Accuracy, Precision, Recall.
- Similarity Score
- Fill – in – the blank (optional)
For further information, please contact : nm.biswas@stud.uis.no
