import sys
import pandas as pd
import joblib
import xgboost as xgb

from colorama import Fore, Style
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from imblearn.under_sampling import RandomUnderSampler


if __name__ == '__main__':
    try:
        print(f'{Fore.GREEN} ===> Reading data...')
        dataframe = pd.read_csv(sys.argv[1], index_col=False)
        features = list(dataframe.columns)
        features.remove('LABEL')
        features.remove('DATETIME')
        y = dataframe['LABEL']
        X = dataframe[features]
        print(' ===> Done')
        
        print(' ===> Encoding labels...')
        label_encoder = LabelEncoder()
        y = label_encoder.fit_transform(y) 
        print(' ===> Done')

        print(' ===> Splitting data...')
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        print(' ===> Done')

        print(' ===> Under sampling...')
        under_sampler = RandomUnderSampler(random_state=42)
        X_train_resampled, y_train_resampled = under_sampler.fit_resample(X_train, y_train)
        print(' ===> Done')

        print(' ===> Training xgb...')
        model = xgb.XGBClassifier(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42)
        model.fit(X_train_resampled, y_train_resampled)
        print(' ===> Done')
      
        print(' ===> Saving model...')
        joblib.dump(model, f'models/xgb_{sys.argv[2]}.pkl')
        joblib.dump(label_encoder, f'models/xgb_label_encoder_{sys.argv[2]}.pkl')
        print(f' ===> Done{Style.RESET_ALL}')

    except Exception as error:
        print(f'{Fore.RED}{error}{Style.RESET_ALL}')