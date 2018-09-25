from flask import Flask, render_template, request
from load import owakati, predict, load_csv, gen_dict, text_to_seq, load_model, np
from get_itunes_review import search, get_review

csv_data = load_csv() # CSVの読み込み
tokenizer = gen_dict(csv_data) # 辞書の作成
model = load_model('./model.h5') # 学習済みモデルをロードする

'''
Kerasのバグらしいので、事前に適当に呼び出しておく
http://tsuwabuki.hatenablog.com/entry/2016/10/17/150033
https://teratail.com/questions/117352
'''
X = np.zeros((10, 400))
model.predict_proba(X, batch_size=32)

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])

def pred_by_review(model=model, tokenizer=tokenizer):
    if request.method == 'GET':
        return render_template('app.html')
    else:
        res = []
        tokenized_text = owakati(request.form['review_text']) # 分かち書きを実行
        vec_text = text_to_seq(tokenized_text, tokenizer)
        res = predict(model, tokenized_text, vec_text)
        return render_template('app.html', input_text=str(request.form['review_text']), result=str(res[0]), array_result=res[1], num_array = res[2])

@app.route('/search', methods=['GET'])

def search_title():
    if request.method == "GET":
        return render_template('search.html')

@app.route('/searchResult', methods=['POST'])

def get_search_result():
    if request.method == "POST":
        search_result = []
        search_result = search(request.form['movie_title'])
        return render_template('search_result.html', results=search_result)

@app.route('/predictViaTitle', methods=['POST'])

def pred_by_title(model=model, tokenizer=tokenizer):
    if request.method == "POST":
        reviews = []
        reviews = get_review(request.form['selectedId'])
        
        pred_results = []
        e = float(0)
        for review in reviews:
            tokenized_text = owakati(review) # 分かち書きを実行
            vec_text = text_to_seq(tokenized_text, tokenizer) # テキストをベクトル化
            res = predict(model, tokenized_text, vec_text) # 予測

            res.insert(0, review) # 配列の先頭に入力したレビューを追加
        
            # 期待値を算出
            prob = res[3]
            print('確率:{}'.format(prob))
            e += 1 * prob[0] + 2 * prob[1]
            print('期待値:{}'.format(1 * prob[0] + 2 * prob[1]))

            pred_results.append(res)
            
        print(pred_results)
        print('期待値の平均:{}'.format(e / len(pred_results)))

        return render_template('predict_result.html', pred_results=pred_results, ex=round(e / len(pred_results), 2))

if __name__ == '__main__':
    app.run(debug=True, port=80)