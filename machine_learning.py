from pyexpat import XML_PARAM_ENTITY_PARSING_ALWAYS
import numpy as np
import pandas as pd
import sklearn
from sklearn.svm import SVR
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.neural_network import MLPRegressor


class MachineLearning(object):

    def __init__(self, df, X_train_cols, y_train_col):
        self.df = df
        self.X_train_cols = X_train_cols
        self.y_train_col = y_train_col

    def LinearRegression(self, new_train):
        regressor = sklearn.linear_model.LinearRegression()
        regressor.fit(self.df[self.X_train_cols], self.df[self.y_train_col])
        df_fit = pd.DataFrame(new_train)
        df_fit_pred = df_fit[self.X_train_cols]
        ratings = regressor.predict(df_fit_pred)
        ratings = [item for sublist in ratings for item in sublist]
        df_fit['rating'] = ratings
        return df_fit.to_dict('records')

    def RandomForestRegression(self, new_train):
        regr = RandomForestRegressor(max_depth=2, random_state=0)
        regr.fit(self.df[self.X_train_cols], self.df[self.y_train_col])
        df_fit = pd.DataFrame(new_train)
        df_fit_pred = df_fit[self.X_train_cols]
        ratings = regr.predict(df_fit_pred)
        ratings = [item for sublist in ratings for item in sublist]
        df_fit['rating'] = ratings
        return df_fit.to_dict('records')

    def NeuralNetwork(self, new_train):
        regr = MLPRegressor(random_state=1, max_iter=500).fit(
            self.df[self.X_train_cols], self.df[self.y_train_col])
        df_fit = pd.DataFrame(new_train)
        df_fit_pred = df_fit[self.X_train_cols]
        ratings = regr.predict(df_fit_pred)
        ratings = [item for sublist in ratings for item in sublist]
        df_fit['rating'] = ratings
        return df_fit.to_dict('records')

    def SVM(self, new_train):
        regr = make_pipeline(StandardScaler(), SVR(C=1.0, epsilon=0.2))
        regr.fit(self.df[self.X_train_cols], self.df[self.y_train_col])
        df_fit = pd.DataFrame(new_train)
        df_fit_pred = df_fit[self.X_train_cols]
        ratings = regr.predict(df_fit_pred)
        ratings = [item for sublist in ratings for item in sublist]
        df_fit['rating'] = ratings
        return df_fit.to_dict('records')

    def kNN(self, new_train):
        neigh = KNeighborsRegressor(n_neighbors=2)
        neigh.fit(self.df[self.X_train_cols], self.df[self.y_train_col])
        df_fit = pd.DataFrame(new_train)
        df_fit_pred = df_fit[self.X_train_cols]
        ratings = neigh.predict(df_fit_pred)
        ratings = [item for sublist in ratings for item in sublist]
        df_fit['rating'] = ratings
        return df_fit.to_dict('records')
