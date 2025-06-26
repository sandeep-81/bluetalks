from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score,confusion_matrix
from sklearn.datasets import load_iris

data =load_iris()
x=data.data
y=data.target
print(y)
X_train , X_test, Y_train, Y_test= train_test_split(x,y, test_size=0.3, random_state=42) 

rf_model= RandomForestClassifier(n_estimators=100, random_state=42)

rf_model.fit(X_train, Y_train)

y_pred= rf_model.predict(X_test)

accuracy= accuracy_score(Y_test,y_pred)
conf_matrix=confusion_matrix(Y_test, y_pred)
print("Accuracy :", accuracy)
print("Confussion metrix : \n",conf_matrix)

