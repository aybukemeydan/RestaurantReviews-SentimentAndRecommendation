# Initialize
import flask
from flask import request, render_template
import pickle
import pandas as pd

app = flask.Flask(__name__,template_folder="templates")

with open('files/cosine_sim.pickle', 'rb') as f:
    cosine_sim = pickle.load(f)


#with open('indices.pickle', 'rb') as f:
#    indices = pickle.load(f)

def get_recommendations(title):
    recommended_restaurant = []  
    indices = pd.read_csv("files/indices.csv")
    indices = indices["name"]
    with open('files/cosine_sim.pickle', 'rb') as f:

        cosine_sim = pickle.load(f)
    # restaurant match indices
    idx = indices[indices == title].index[0]
    # similarity scores
    score_series = pd.Series(cosine_sim[idx]).sort_values(ascending = False)
    # top n
    top_n_indexes = list(score_series.iloc[1:11].index)
    for i in top_n_indexes:
        recommended_restaurant.append(list(indices)[i])
     #df = pd.DataFrame(recommended_restaurant)   
    return recommended_restaurant


# Set up the main route , methods=['GET', 'POST']
@app.route('/predict', methods=['GET', 'POST'])
def main():

    
    if request.method == 'GET':
        return(flask.send_file('templates/index.html'))
            
    if request.method == 'POST':
        try:
            m_name = request.form['movie_name']
            m_name =" "+m_name
            result_final = get_recommendations(m_name)
            names = []
            for i in range(len(result_final)):
                names.append(result_final[i])

            return render_template('positive.html',movie_names=names,search_name=m_name)
        except:
            
            return render_template("negative.html",name=m_name)
 
  
 

if __name__=="__main__":
    app.run(debug=True)
