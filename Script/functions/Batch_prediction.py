from osgeo import gdal

from fastbook import *
from pandas.api.types import is_string_dtype, is_numeric_dtype, is_categorical_dtype
from fastai.tabular.all import *
pd.options.display.max_rows = 20
pd.options.display.max_columns = 8
import numpy as np
from matplotlib import colors

import matplotlib.pyplot as plt
import warnings
import pandas as d
warnings.filterwarnings("ignore")

def scaleMinMax(x):
    return((x-np.nanmin(x))/(np.nanmax(x)-np.nanmin(x)))

def scaleCCC(x):
    return((x- np.nanpercentile(x,0))/(np.nanpercentile(x,98)-np.nanpercentile(x,0)))

def batch_prediction(imgs, models):


    for img_i in imgs:

        print(img_i)
        lowtif = gdal.Open('../Data/img/' + img_i + '.tif')
        gt = lowtif.GetGeoTransform()
        proj = lowtif.GetProjection()

        Reflectance_444 = lowtif.GetRasterBand(1).ReadAsArray().astype('float')
        Reflectance_475 = lowtif.GetRasterBand(2).ReadAsArray().astype('float')
        Reflectance_531 = lowtif.GetRasterBand(3).ReadAsArray().astype('float')
        Reflectance_560 = lowtif.GetRasterBand(4).ReadAsArray().astype('float')
        Reflectance_650 = lowtif.GetRasterBand(5).ReadAsArray().astype('float')
        Reflectance_668 = lowtif.GetRasterBand(6).ReadAsArray().astype('float')
        Reflectance_705 = lowtif.GetRasterBand(7).ReadAsArray().astype('float')
        Reflectance_717 = lowtif.GetRasterBand(8).ReadAsArray().astype('float')
        Reflectance_740 = lowtif.GetRasterBand(9).ReadAsArray().astype('float')
        Reflectance_842 = lowtif.GetRasterBand(10).ReadAsArray().astype('float')

        lowtif = None

        Reflectance_444[Reflectance_444 == 65535] = np.NAN
        Reflectance_475[Reflectance_475 == 65535] = np.NAN
        Reflectance_531[Reflectance_531 == 65535] = np.NAN
        Reflectance_560[Reflectance_560 == 65535] = np.NAN
        Reflectance_650[Reflectance_650 == 65535] = np.NAN
        Reflectance_668[Reflectance_668 == 65535] = np.NAN
        Reflectance_705[Reflectance_705 == 65535] = np.NAN
        Reflectance_717[Reflectance_717 == 65535] = np.NAN
        Reflectance_740[Reflectance_740 == 65535] = np.NAN
        Reflectance_842[Reflectance_842 == 65535] = np.NAN

        Reflectance_444[Reflectance_444 == 0] = np.NAN
        Reflectance_475[Reflectance_475 == 0] = np.NAN
        Reflectance_531[Reflectance_531 == 0] = np.NAN
        Reflectance_560[Reflectance_560 == 0] = np.NAN
        Reflectance_650[Reflectance_650 == 0] = np.NAN
        Reflectance_668[Reflectance_668 == 0] = np.NAN
        Reflectance_705[Reflectance_705 == 0] = np.NAN
        Reflectance_717[Reflectance_717 == 0] = np.NAN
        Reflectance_740[Reflectance_740 == 0] = np.NAN
        Reflectance_842[Reflectance_842 == 0] = np.NAN

        Full = np.dstack((Reflectance_444,Reflectance_475,Reflectance_531,Reflectance_560,Reflectance_650,
                        Reflectance_668,Reflectance_705,Reflectance_717,Reflectance_740,Reflectance_842))
        
        if os.path.isfile("../Data/np_arrays/" + img_i + "_Stan.npy"):
            print("File exists! Opening the Numpy Array")
            FullStan = np.load("../Data/np_arrays/" + img_i + "_Stan.npy")
        else:
            print("File does not exist! Perform operations on the data array...")
            FullStan=np.apply_along_axis(scaleMinMax, 2, Full)
            np.save("../Data/np_arrays/" + img_i + "_Stan",FullStan)
        
        Full_ten = torch.from_numpy(Full)
        FullStan_ten =torch.from_numpy(FullStan)    

        NDVI=(Full_ten[:,:,9]-Full_ten[:,:,5])/(Full_ten[:,:,9]+Full_ten[:,:,5])
        NDVI=NDVI[:,:,None]

        NDVI_Stan=(FullStan_ten[:,:,9]-FullStan_ten[:,:,5])/(FullStan_ten[:,:,9]+FullStan_ten[:,:,5])
        NDVI_Stan=NDVI_Stan[:,:,None]

        FullCombo_ten=torch.cat((Full_ten,FullStan_ten,NDVI,NDVI_Stan),2)

        Full_ten = None
        NDVI_Stan = None
        NDVI = None
        Reflectance_444= None
        Reflectance_475= None
        Reflectance_531= None
        Reflectance_560= None
        Reflectance_650= None
        Reflectance_668= None
        Reflectance_705= None
        Reflectance_717= None
        Reflectance_740= None
        Reflectance_842= None
        FullStan= None

        Columns_test=['Reflectance_444',
              'Reflectance_475',
              'Reflectance_531',
              'Reflectance_560',
              'Reflectance_650',
              'Reflectance_668',
              'Reflectance_705',
              'Reflectance_717',
              'Reflectance_740',
              'Reflectance_842',
              'Reflectance_Stan_444',
              'Reflectance_Stan_475',
              'Reflectance_Stan_531',
              'Reflectance_Stan_560',
              'Reflectance_Stan_650',
              'Reflectance_Stan_668',
              'Reflectance_Stan_705',
              'Reflectance_Stan_717',
              'Reflectance_Stan_740',
              'Reflectance_Stan_842',
              'NDVI',
              'NDVI_Stan']
        
        v = FullCombo_ten.view(FullCombo_ten.shape[0]*FullCombo_ten.shape[1],FullCombo_ten.shape[2])

        df_test_nan=pd.DataFrame(v,columns=Columns_test)
        df_test_nan_nrum = df_test_nan

        v = None

        df_test = df_test_nan.dropna()

        df_test_nan_nrum['ID'] = np.arange(len(df_test_nan_nrum))
        df_test_nrum = df_test_nan_nrum.dropna()

        df_test_nan_nrum = None

        ID_l=list(df_test_nrum['ID'])

        for learn_i in models:
            print(learn_i)

            learn = load_learner('../models/' + learn_i + '.pkl')
            categories = learn.dls.vocab
            learn = None

            dl = learn.dls.test_dl(df_test, bs=4000)
            preds,_ = learn.get_preds(dl=dl)

            dl= None

            class_idxs = preds.argmax(axis=1)

            class_probs= preds.max(axis=1)

            preds = None

            class_probs=class_probs.values

            NumPred= class_idxs.tolist()
            PredProbs =class_probs.tolist()

            class_idxs = None
            class_probs = None

            res_df= pd.DataFrame(list(zip(NumPred, ID_l,PredProbs)),columns =['Pred_ID','ID','Prob'])

            df_test_nan1['ID']= np.arange(len(df_test_nan))

            res_input_df = pd.merge(df_test_nan,res_df, how='left', on = 'ID')

            res_df = None

            Pred_arr = np.asarray(res_input_df['Pred_ID'])

            Pred_arr=Pred_arr+1

            Prob_arr = np.asarray(res_input_df['Prob'])

            res_input_df = None

            Prob_ras = Prob_arr.reshape(Full.shape[0], Full.shape[1])

            Pred_ras = Pred_arr.reshape(Full.shape[0], Full.shape[1])

            Pred_arr = None
            Prob_arr = None

            # export
            driver = gdal.GetDriverByName("GTiff")
            driver.Register()
            outds = driver.Create("../Output/Pred/Batch/" + img_i + '_' + learn_i +"_prob.tif", xsize = Prob_ras.shape[1],
                                ysize = Prob_ras.shape[0], bands = 1, 
                                eType = gdal.GDT_Float32)

            outds.SetGeoTransform(gt)
            outds.SetProjection(proj)
            outband = outds.GetRasterBand(1)
            outband.WriteArray(Prob_ras)
            outband.SetNoDataValue(65535)
            outband.FlushCache()

            # close your datasets and bands!!!
            outband = None
            outds = None

            driver = gdal.GetDriverByName("GTiff")
            driver.Register()
            outds = driver.Create("../Output/Pred/Batch/" + img_i + '_' + learn_i +"_pred.tif", xsize = Pred_ras.shape[1],
                                ysize = Pred_ras.shape[0], bands = 1, 
                                eType = gdal.GDT_Int16)
            outds.SetGeoTransform(gt)
            outds.SetProjection(proj)
            outband = outds.GetRasterBand(1)
            outband.WriteArray(Pred_ras)
            outband.SetNoDataValue(65535)
            outband.SetNoDataValue(32767)
            outband.FlushCache()
            # close your datasets and bands!!!
            outband = None
            outds = None

            dl = None
            preds = None
            class_idxs = None
            class_probs = None
            NumPred = None
            PredProbs = None
            res_df = None
            res_input_df = None
            res_input_df_Nan = None
            Pred_arr = None
            Prob_ras = None
            driver = None

