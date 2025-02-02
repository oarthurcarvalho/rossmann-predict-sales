import os
import pickle
import pandas       as pd
import numpy        as np
import datetime
import inflection

from math          import isnan

class Rossmann( object ):
    def __init__( self ):
        # Define the base path relative to the current file location
        base_path = os.path.dirname(os.path.abspath(__file__))
        
        # Load the scalers using relative paths
        self.scaler_competition_distance = pickle.load( open( os.path.join(base_path, '../../parameter/scaler_competition_distance.pkl'), 'rb' ) )
        self.scaler_competition_time_month = pickle.load( open( os.path.join(base_path, '../../parameter/scaler_competition_time_month.pkl'), 'rb' ) )
        self.scaler_promo_time_week = pickle.load( open( os.path.join(base_path, '../../parameter/scaler_promo_time_week.pkl'), 'rb' ) )
        self.scaler_year = pickle.load( open( os.path.join(base_path, '../../parameter/scaler_year.pkl'), 'rb' ) )
        self.scaler_store_type = pickle.load( open( os.path.join(base_path, '../../parameter/store_type_scaler.pkl'), 'rb' ) )

    def data_cleaning( self, df1 ):

        # RENAME COLUMNS
        cols_old = list(df1.columns)
        snakecase = lambda x: inflection.underscore( x )
        cols_new = list( map( snakecase, cols_old ) )
        df1.columns = cols_new

        # CONVERT DATE COLUMN TO DATETIME
        df1['date'] = pd.to_datetime( df1['date'] )

        # FILL OUT NA
        
        # competition_distance
        df1['competition_distance'] = df1['competition_distance'].apply( lambda x: 200000.0 if isnan( x ) else x )
        
        # competition_open_since_month
        df1['competition_open_since_month'] = df1.apply( 
            lambda x: x['date'].month 
                if isnan( x['competition_open_since_month'] ) 
                else x['competition_open_since_month'],
            axis=1
        )
        
        # competition_open_since_year
        df1['competition_open_since_year'] = df1.apply( 
            lambda x: x['date'].year 
                if isnan( x['competition_open_since_year'] ) 
                else x['competition_open_since_year'],
            axis=1
        )
        
        # promo2_since_week
        df1['promo2_since_week'] = df1.apply( 
            lambda x: x['date'].week 
                if isnan( x['promo2_since_week'] ) 
                else x['promo2_since_week'],
            axis=1
        )
        
        # promo2_since_year
        df1['promo2_since_year'] = df1.apply( 
            lambda x: x['date'].year
                if isnan( x['promo2_since_year'] ) 
                else x['promo2_since_year'],
            axis=1
        )
        
        # promo_interval
        month_map = { 1: 'Jan', 2: ' Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
                      7: 'Jul', 8: 'Aug', 9: 'Sept', 10: 'Oct', 11: 'Nov', 12: 'Dec'
                    }
        df1['promo_interval'] = df1['promo_interval'].fillna(0)
        
        df1['month_map'] = df1['date'].dt.month.map( month_map )
        
        df1['is_promo'] = df1[['promo_interval', 'month_map']].apply(
            lambda x: 0 if x['promo_interval'] == 0 else 1 
                if x['month_map'] in x['promo_interval'].split( ',' ) else 0,
            axis=1 
        )

        df1['competition_open_since_month'] = df1['competition_open_since_month'].astype( int )
        df1['competition_open_since_year'] = df1['competition_open_since_year'].astype( int )
        
        df1['promo2_since_week'] = df1['promo2_since_week'].astype( int )
        df1['promo2_since_year'] = df1['promo2_since_year'].astype( int )

        return df1


    def feature_engineering( self, df2 ):
        
        # year
        df2['year'] = df2['date'].dt.year
        
        # month
        df2['month'] = df2['date'].dt.month
        
        # day
        df2['day'] = df2['date'].dt.day
        
        # week of year
        df2['week_of_year'] = df2['date'].dt.isocalendar().week
        
        # year week
        df2['year_week'] = df2['date'].dt.strftime( '%Y-%W' )
        
        # competition since
        df2['competition_since'] = df2.apply(
            lambda x: datetime.datetime( 
                year=x['competition_open_since_year'],
                month=x['competition_open_since_month'],
                day=1
            ),
            axis=1
        )
        df2['competition_time_month'] = ( 
            ( df2['date'] - df2['competition_since'] ) / 30 
            ).apply( lambda x: x.days ).astype( int )
        
        # promo since
        df2['promo_since'] = df2['promo2_since_year'].astype( str ) + '-' + df2['promo2_since_week'].astype( str )
        df2['promo_since'] = df2['promo_since'].apply( lambda x: datetime.datetime.strptime( x + '-1', '%Y-%W-%w' ) - datetime.timedelta( days=7 ) )
        df2['promo_time_week'] = ( ( df2['date'] - df2['promo_since'] ) / 7 ).apply( lambda x: x.days ).astype( int )
        
        # assortment
        assortment_map = {
            'a': 'basic',
            'b': 'extra',
            'c': 'extended'
        }
        df2['assortment'] = df2['assortment'].map(assortment_map)
        
        # state holiday
        state_holiday_map = {
            'a': 'public holiday',
            'b': 'Easter holiday',
            'c': 'Christmas',
            '0': 'regular_day'
        }
        df2['state_holiday'] = df2['state_holiday'].map(state_holiday_map)
        
        # FILTERING
        df2 = df2[( df2['open'] != 0 ) ]
        
        cols_drop = ['open', 'promo_interval', 'month_map']
        df2 = df2.drop( cols_drop, axis=1 )

        return df2

    def data_preparation( self, df5 ):
        
        # competition distance
        df5['competition_distance'] = self.scaler_competition_distance.transform( df5[['competition_distance']].values )
        
        # competition time month
        df5['competition_time_month'] = self.scaler_competition_time_month.transform( df5[['competition_time_month']].values )
        
        # promo time week
        df5['promo_time_week'] = self.scaler_promo_time_week.transform( df5[['promo_time_week']].values )

        # year 
        df5['year'] = self.scaler_year.transform( df5[['year']].values )
        
        ### 5.3.1. Encoding
        
        # state_holiday - One Hot Encoding
        df5 = pd.get_dummies( df5, prefix=['state_holiday'], columns=['state_holiday'], dtype=int )
        
        # store_type - Label Encoding
        df5['store_type'] = self.scaler_store_type.transform( df5['store_type'] )
        
        
        # assortment - Ordinal Encoding
        assortment_dict = {'basic': 1, 'extra': 2, 'extended': 3}
        df5['assortment'] = df5['assortment'].map( assortment_dict )
        
        # Nature Transformation
        
        # day_of_week
        df5['day_of_week_sin'] = df5['day_of_week'].apply( lambda x: np.sin( x * ( 2. * np.pi/7 ) ) )
        df5['day_of_week_cos'] = df5['day_of_week'].apply( lambda x: np.cos( x * ( 2. * np.pi/7 ) ) )
        
        # month
        df5['month_sin'] = df5['month'].apply( lambda x: np.sin( x * ( 2. * np.pi/12 ) ) )
        df5['month_cos'] = df5['month'].apply( lambda x: np.cos( x * ( 2. * np.pi/12 ) ) )
        
        # day
        df5['day_sin'] = df5['day'].apply( lambda x: np.sin( x * ( 2. * np.pi/30 ) ) )
        df5['day_cos'] = df5['day'].apply( lambda x: np.cos( x * ( 2. * np.pi/30 ) ) )
        
        # week_of_year
        df5['week_of_year_sin'] = df5['week_of_year'].apply( lambda x: np.sin( x * ( 2. * np.pi/52 ) ) )
        df5['week_of_year_cos'] = df5['week_of_year'].apply( lambda x: np.cos( x * ( 2. * np.pi/52 ) ) )

        cols_selected_boruta = [ 'store', 'promo', 'store_type', 'assortment', 'competition_distance',
                                 'competition_open_since_month', 'competition_open_since_year', 'promo2',
                                 'promo2_since_week', 'promo2_since_year', 'competition_time_month',
                                 'promo_time_week', 'day_of_week_sin', 'day_of_week_cos', 'month_cos',
                                 'month_sin', 'day_sin', 'day_cos', 'week_of_year_cos', 'week_of_year_sin'
                                ]
        
        return df5[cols_selected_boruta]

    def get_prediction( self, model, original_data, test_data ):
        # prediction
        pred = model.predict( test_data )

        # join pred into the original data
        original_data['prediction'] = np.expm1( pred )

        return original_data.to_json( orient='records', date_format='iso' )
