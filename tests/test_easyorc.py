import easyocr

reader = easyocr.Reader(['ch_sim', 'en'])  # this needs to run only once to load the model into memory
print('inited reader')
result = reader.readtext('../static/img/test_chinese_2.png')

print(result)
