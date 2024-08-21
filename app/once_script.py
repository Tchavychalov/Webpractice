from transformers import AutoModelForSequenceClassification, BertTokenizerFast

model_name = 'blanchefort/rubert-base-cased-sentiment-med'
tokenizer = BertTokenizerFast.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

tokenizer.save_pretrained('./model/tokenizer')
model.save_pretrained('./model')
