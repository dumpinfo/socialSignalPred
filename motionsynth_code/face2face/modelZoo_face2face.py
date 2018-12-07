import os
import sys
import numpy as np
import scipy.io as io

rng = np.random.RandomState(23456)

import torch
import torchvision
from torch import nn
from torch.autograd import Variable
from torch.utils.data import DataLoader
from torchvision import transforms
from torchvision.utils import save_image
from torchvision.datasets import MNIST
import os


def make_mlp(dim_list, activation='relu', batch_norm=True, dropout=0):
    layers = []
    for dim_in, dim_out in zip(dim_list[:-1], dim_list[1:]):
        layers.append(nn.Linear(dim_in, dim_out))
        if batch_norm:
            layers.append(nn.BatchNorm1d(dim_out))
        if activation == 'relu':
            layers.append(nn.ReLU())
        elif activation == 'leakyrelu':
            layers.append(nn.LeakyReLU())
        if dropout > 0:
            layers.append(nn.Dropout(p=dropout))
    return nn.Sequential(*layers)



class autoencoder_first(nn.Module):
    def __init__(self, featureDim):
        super(autoencoder_first, self).__init__()
        self.encoder = nn.Sequential(
            nn.Dropout(0.25),
            nn.Conv1d(featureDim,256,25,padding=12),        #256, 73, 200
            nn.ReLU(True),
            nn.MaxPool1d(kernel_size=2, stride=2)   #256, 73, 120
        )
        self.decoder = nn.Sequential(
            #nn.MaxUnpool1d(kernel_size=2, stride=2),
            nn.Dropout(0.25),
            nn.ConvTranspose1d(256, featureDim, 25, stride=2, padding=12, output_padding=1),
            #nn.ReLU(True)
          )  

    def forward(self, x):
        x = self.encoder(x)
        x = self.decoder(x)
        return x





class naive_mlp(nn.Module):
    def __init__(self):
        super(naive_mlp, self).__init__()

        self.feature_dim= 3
        self.output_dim = 69
        
        mlp_dims = [self.feature_dim, 20]
        activation='relu'
        dropout=0
        batch_norm = True
        self.mlp = make_mlp(
                mlp_dims,
                activation=activation,
                batch_norm=batch_norm,
                dropout=dropout
            )

        self.proj = nn.Linear(mlp_dims[-1],self.output_dim)

    def forward(self, input_):

        output = self.mlp(input_)
        return self.proj(output)




class regressor_fcn_bn_encoder_2(nn.Module):
    def __init__(self):
        super(regressor_fcn_bn_encoder_2, self).__init__()

        self.encoder = nn.Sequential(
            nn.Dropout(0.25),
            nn.Conv1d(146,256,3,padding=1),        #256, 73, 200
            nn.ReLU(),
            nn.BatchNorm1d(256),

            nn.Dropout(0.25),
            nn.Conv1d(256,256,3,padding=1),        #256, 73, 200
            nn.ReLU(),
            nn.BatchNorm1d(256),

            nn.Dropout(0.25),
            nn.Conv1d(256,256,3,padding=1),        #256, 73, 200
            nn.ReLU(),
            nn.BatchNorm1d(256),
            nn.MaxPool1d(kernel_size=2, stride=2),   #256, 73, 120
        )

        # self.decoder = nn.Sequential(
        #     #nn.MaxUnpool1d(kernel_size=2, stride=2),
        #     nn.Dropout(0.25),
        #     nn.ConvTranspose1d(256, 73, 25, stride=2, padding=12, output_padding=1),
        #     #nn.ReLU(True)
        #   )  

    def forward(self, input_):
        latent = self.encoder(input_)
        #output = self.decoder(latent)
        #return output
        return latent



class regressor_fcn_bn_encoder_5(nn.Module):
    def __init__(self):
        super(regressor_fcn_bn_encoder_5, self).__init__()

        self.encoder = nn.Sequential(
            nn.Dropout(0.25),
            nn.Conv1d(146,256,5,padding=2),        #256, 73, 200
            nn.ReLU(),
            nn.BatchNorm1d(256),

            nn.Dropout(0.25),
            nn.Conv1d(256,256,5,padding=2),        #256, 73, 200
            nn.ReLU(),
            nn.BatchNorm1d(256),

            nn.Dropout(0.25),
            nn.Conv1d(256,256,5,padding=2),        #256, 73, 200
            nn.ReLU(),
            nn.BatchNorm1d(256),
            nn.MaxPool1d(kernel_size=2, stride=2),   #256, 73, 120
        )

        # self.decoder = nn.Sequential(
        #     #nn.MaxUnpool1d(kernel_size=2, stride=2),
        #     nn.Dropout(0.25),
        #     nn.ConvTranspose1d(256, 73, 25, stride=2, padding=12, output_padding=1),
        #     #nn.ReLU(True)
        #   )  

    def forward(self, input_):
        latent = self.encoder(input_)
        #output = self.decoder(latent)
        #return output
        return latent


class regressor_fcn_bn_encoder_7(nn.Module):
    def __init__(self):
        super(regressor_fcn_bn_encoder_7, self).__init__()

        self.encoder = nn.Sequential(
            nn.Dropout(0.25),
            nn.Conv1d(146,256,7,padding=3),        #256, 73, 200
            nn.ReLU(),
            nn.BatchNorm1d(256),

            nn.Dropout(0.25),
            nn.Conv1d(256,256,7,padding=3),        #256, 73, 200
            nn.ReLU(),
            nn.BatchNorm1d(256),

            nn.Dropout(0.25),
            nn.Conv1d(256,256,7,padding=3),        #256, 73, 200
            nn.ReLU(),
            nn.BatchNorm1d(256),
            nn.MaxPool1d(kernel_size=2, stride=2),   #256, 73, 120
        )

        # self.decoder = nn.Sequential(
        #     #nn.MaxUnpool1d(kernel_size=2, stride=2),
        #     nn.Dropout(0.25),
        #     nn.ConvTranspose1d(256, 73, 25, stride=2, padding=12, output_padding=1),
        #     #nn.ReLU(True)
        #   )  

    def forward(self, input_):
        latent = self.encoder(input_)
        #output = self.decoder(latent)
        #return output
        return latent



class regressor_fcn_bn(nn.Module):
    def __init__(self):
        super(regressor_fcn_bn, self).__init__()

        self.encoder = nn.Sequential(
            nn.Dropout(0.25),
            nn.Conv1d(146,256,45,padding=22),        #256, 73, 200
            nn.ReLU(),
            nn.BatchNorm1d(256),

            nn.Dropout(0.25),
            nn.Conv1d(256,256,25,padding=12),        #256, 73, 200
            nn.ReLU(),
            nn.BatchNorm1d(256),

            nn.Dropout(0.25),
            nn.Conv1d(256,256,15,padding=7),        #256, 73, 200
            nn.ReLU(),
            nn.BatchNorm1d(256),
            nn.MaxPool1d(kernel_size=2, stride=2),   #256, 73, 120
        )

        self.decoder = nn.Sequential(
            #nn.MaxUnpool1d(kernel_size=2, stride=2),
            nn.Dropout(0.25),
            nn.ConvTranspose1d(256, 73, 25, stride=2, padding=12, output_padding=1),
            #nn.ReLU(True)
          )  

    def forward(self, input_):
        latent = self.encoder(input_)
        output = self.decoder(latent)
        return output



class regressor_fcn_bn_noDrop(nn.Module):
    def __init__(self):
        super(regressor_fcn_bn_noDrop, self).__init__()

        self.encoder = nn.Sequential(
            #nn.Dropout(0.25),
            nn.Conv1d(146,256,45,padding=22),        #256, 73, 200
            nn.ReLU(),
            nn.BatchNorm1d(256),

            #nn.Dropout(0.25),
            nn.Conv1d(256,256,25,padding=12),        #256, 73, 200
            nn.ReLU(),
            nn.BatchNorm1d(256),

            #nn.Dropout(0.25),
            nn.Conv1d(256,256,15,padding=7),        #256, 73, 200
            nn.ReLU(),
            nn.BatchNorm1d(256),
            nn.MaxPool1d(kernel_size=2, stride=2),   #256, 73, 120
        )

        self.decoder = nn.Sequential(
            #nn.MaxUnpool1d(kernel_size=2, stride=2),
            #nn.Dropout(0.25),
            nn.ConvTranspose1d(256, 73, 25, stride=2, padding=12, output_padding=1),
            #nn.ReLU(True)
          )  

    def forward(self, input_):
        latent = self.encoder(input_)
        output = self.decoder(latent)
        return output



class regressor_fcn_bn_2(nn.Module):
    def __init__(self):
        super(regressor_fcn_bn_2, self).__init__()

        self.encoder = nn.Sequential(
            nn.Dropout(0.25),
            nn.Conv1d(146,256,45,padding=22),        #256, 73, 200
            nn.ReLU(),
            nn.BatchNorm1d(256),

            nn.Dropout(0.25),
            nn.Conv1d(256,512,25,padding=12),        #256, 73, 200
            nn.ReLU(),
            nn.BatchNorm1d(512),

            nn.Dropout(0.25),
            nn.Conv1d(512,512,15,padding=7),        #256, 73, 200
            nn.ReLU(),
            nn.BatchNorm1d(512),
            nn.MaxPool1d(kernel_size=2, stride=2),   #256, 73, 120
        )

        self.decoder = nn.Sequential(
            #nn.MaxUnpool1d(kernel_size=2, stride=2),
            nn.Dropout(0.25),
            nn.ConvTranspose1d(512, 73, 25, stride=2, padding=12, output_padding=1),
            #nn.ReLU(True)
          )  

    def forward(self, input_):
        latent = self.encoder(input_)
        output = self.decoder(latent)
        return output



class regressor_fcn_bn_3(nn.Module):
    def __init__(self):
        super(regressor_fcn_bn_3, self).__init__()

        self.encoder = nn.Sequential(
            nn.Dropout(0.25),
            nn.Conv1d(146,256,45,padding=22),        #256, 73, 200
            nn.ReLU(),
            nn.BatchNorm1d(256),

            nn.Dropout(0.25),
            nn.Conv1d(256,512,25,padding=12),        #256, 73, 200
            nn.ReLU(),
            nn.BatchNorm1d(512),

            nn.Dropout(0.25),
            nn.Conv1d(512,1024,15,padding=7),        #256, 73, 200
            nn.ReLU(),
            nn.BatchNorm1d(1024),
            nn.MaxPool1d(kernel_size=2, stride=2),   #256, 73, 120
        )

        self.decoder = nn.Sequential(
            #nn.MaxUnpool1d(kernel_size=2, stride=2),
            nn.Dropout(0.25),
            nn.ConvTranspose1d(1024, 73, 25, stride=2, padding=12, output_padding=1),
            #nn.ReLU(True)
          )  

    def forward(self, input_):
        latent = self.encoder(input_)
        output = self.decoder(latent)
        return output




class regressor_fcn_bn(nn.Module):
    def __init__(self):
        super(regressor_fcn_bn, self).__init__()

        self.encoder = nn.Sequential(
            nn.Dropout(0.25),
            nn.Conv1d(146,256,45,padding=22),        #256, 73, 200
            nn.ReLU(),
            nn.BatchNorm1d(256),

            nn.Dropout(0.25),
            nn.Conv1d(256,256,25,padding=12),        #256, 73, 200
            nn.ReLU(),
            nn.BatchNorm1d(256),

            nn.Dropout(0.25),
            nn.Conv1d(256,256,15,padding=7),        #256, 73, 200
            nn.ReLU(),
            nn.BatchNorm1d(256),
            nn.MaxPool1d(kernel_size=2, stride=2),   #256, 73, 120
        )

        self.decoder = nn.Sequential(
            #nn.MaxUnpool1d(kernel_size=2, stride=2),
            nn.Dropout(0.25),
            nn.ConvTranspose1d(256, 73, 25, stride=2, padding=12, output_padding=1),
            #nn.ReLU(True)
          )  

    def forward(self, input_):
        latent = self.encoder(input_)
        output = self.decoder(latent)
        return output


class regressor_fcn_bn_noDrop(nn.Module):
    def __init__(self):
        super(regressor_fcn_bn_noDrop, self).__init__()

        self.encoder = nn.Sequential(
            #nn.Dropout(0.25),
            nn.Conv1d(146,256,45,padding=22),        #256, 73, 200
            nn.ReLU(),
            nn.BatchNorm1d(256),

            #nn.Dropout(0.25),
            nn.Conv1d(256,256,25,padding=12),        #256, 73, 200
            nn.ReLU(),
            nn.BatchNorm1d(256),

            #nn.Dropout(0.25),
            nn.Conv1d(256,256,15,padding=7),        #256, 73, 200
            nn.ReLU(),
            nn.BatchNorm1d(256),
            nn.MaxPool1d(kernel_size=2, stride=2),   #256, 73, 120
        )

        self.decoder = nn.Sequential(
            #nn.MaxUnpool1d(kernel_size=2, stride=2),
            #nn.Dropout(0.25),
            nn.ConvTranspose1d(256, 73, 25, stride=2, padding=12, output_padding=1),
            #nn.ReLU(True)
          )  

    def forward(self, input_):
        latent = self.encoder(input_)
        output = self.decoder(latent)
        return output



class regressor_fcn_bn_2(nn.Module):
    def __init__(self):
        super(regressor_fcn_bn_2, self).__init__()

        self.encoder = nn.Sequential(
            nn.Dropout(0.25),
            nn.Conv1d(146,256,45,padding=22),        #256, 73, 200
            nn.ReLU(),
            nn.BatchNorm1d(256),

            nn.Dropout(0.25),
            nn.Conv1d(256,512,25,padding=12),        #256, 73, 200
            nn.ReLU(),
            nn.BatchNorm1d(512),

            nn.Dropout(0.25),
            nn.Conv1d(512,512,15,padding=7),        #256, 73, 200
            nn.ReLU(),
            nn.BatchNorm1d(512),
            nn.MaxPool1d(kernel_size=2, stride=2),   #256, 73, 120
        )

        self.decoder = nn.Sequential(
            #nn.MaxUnpool1d(kernel_size=2, stride=2),
            nn.Dropout(0.25),
            nn.ConvTranspose1d(512, 73, 25, stride=2, padding=12, output_padding=1),
            #nn.ReLU(True)
          )  

    def forward(self, input_):
        latent = self.encoder(input_)
        output = self.decoder(latent)
        return output



class regressor_fcn_bn_encoder(nn.Module):
    def __init__(self):
        super(regressor_fcn_bn_encoder, self).__init__()

        self.encoder = nn.Sequential(
            nn.Dropout(0.25),
            nn.Conv1d(10,64,25,padding=12),        #256, 73, 200
            nn.ReLU(),
            nn.BatchNorm1d(64),

            nn.Dropout(0.25),
            nn.Conv1d(64,128,15,padding=7),        #256, 73, 200
            nn.ReLU(),
            nn.BatchNorm1d(128),

            nn.Dropout(0.25),
            nn.Conv1d(128,256,5,padding=2),        #256, 73, 200
            nn.ReLU(),
            #nn.BatchNorm1d(256),
            nn.MaxPool1d(kernel_size=2, stride=2),   #256, 73, 120
        )

        # self.decoder = nn.Sequential(
        #     #nn.MaxUnpool1d(kernel_size=2, stride=2),
        #     nn.Dropout(0.25),
        #     nn.ConvTranspose1d(256, 73, 25, stride=2, padding=12, output_padding=1),
        #     #nn.ReLU(True)
        #   )  

    def forward(self, input_):
        latent = self.encoder(input_)
        return latent


class regressor_fcn_bn_encoder_2(nn.Module):
    def __init__(self):
        super(regressor_fcn_bn_encoder_2, self).__init__()

        self.encoder = nn.Sequential(
            nn.Dropout(0.25),
            nn.Conv1d(10,64,3,padding=1),        #256, 73, 200
            nn.ReLU(),
            nn.BatchNorm1d(64),

            nn.Dropout(0.25),
            nn.Conv1d(64,128,3,padding=1),        #256, 73, 200
            nn.ReLU(),
            nn.BatchNorm1d(128),

            nn.Dropout(0.25),
            nn.Conv1d(128,256,3,padding=1),        #256, 73, 200
            nn.ReLU(),
            #nn.BatchNorm1d(256),
            nn.MaxPool1d(kernel_size=2, stride=2),   #256, 73, 120
        )

        # self.decoder = nn.Sequential(
        #     #nn.MaxUnpool1d(kernel_size=2, stride=2),
        #     nn.Dropout(0.25),
        #     nn.ConvTranspose1d(256, 73, 25, stride=2, padding=12, output_padding=1),
        #     #nn.ReLU(True)
        #   )  

    def forward(self, input_):
        latent = self.encoder(input_)
        return latent


class regressor_fcn_bn_encoder_noDrop(nn.Module):
    def __init__(self):
        super(regressor_fcn_bn_encoder_noDrop, self).__init__()

        self.encoder = nn.Sequential(
            #nn.Dropout(0.25),
            nn.Conv1d(10,64,25,padding=12),        #256, 73, 200
            nn.ReLU(),
            nn.BatchNorm1d(64),

            #nn.Dropout(0.25),
            nn.Conv1d(64,128,15,padding=7),        #256, 73, 200
            nn.ReLU(),
            nn.BatchNorm1d(128),

            #nn.Dropout(0.25),
            nn.Conv1d(128,256,5,padding=2),        #256, 73, 200
            nn.ReLU(),
            nn.BatchNorm1d(256),
            nn.MaxPool1d(kernel_size=2, stride=2),   #256, 73, 120
        )

        # self.decoder = nn.Sequential(
        #     #nn.MaxUnpool1d(kernel_size=2, stride=2),
        #     nn.Dropout(0.25),
        #     nn.ConvTranspose1d(256, 73, 25, stride=2, padding=12, output_padding=1),
        #     #nn.ReLU(True)
        #   )  

    def forward(self, input_):
        latent = self.encoder(input_)
        return latent


#doesnt work
class regressor_fcn_bn_encoder_noDrop_2(nn.Module):
    def __init__(self):
        super(regressor_fcn_bn_encoder_noDrop_2, self).__init__()

        self.encoder = nn.Sequential(
            #nn.Dropout(0.25),
            nn.Conv1d(10,256,25,padding=12),        #256, 73, 200
            nn.ReLU(),
            nn.BatchNorm1d(256),
            nn.MaxPool1d(kernel_size=2, stride=2)   #256, 73, 120
        )

        # self.decoder = nn.Sequential(
        #     #nn.MaxUnpool1d(kernel_size=2, stride=2),
        #     nn.Dropout(0.25),
        #     nn.ConvTranspose1d(256, 73, 25, stride=2, padding=12, output_padding=1),
        #     #nn.ReLU(True)
        #   )  

    def forward(self, input_):
        latent = self.encoder(input_)
        return latent




class regressor_fcn_bn_encoder_noDrop_3(nn.Module):
    def __init__(self):
        super(regressor_fcn_bn_encoder_noDrop_3, self).__init__()

        self.encoder = nn.Sequential(
            #nn.Dropout(0.25),
            nn.Conv1d(10,64,3,padding=1),        #256, 73, 200
            nn.ReLU(),
            nn.BatchNorm1d(64),

            #nn.Dropout(0.25),
            nn.Conv1d(64,128,3,padding=1),        #256, 73, 200
            nn.ReLU(),
            nn.BatchNorm1d(128),

            #nn.Dropout(0.25),
            nn.Conv1d(128,256,3,padding=1),        #256, 73, 200
            nn.ReLU(),
            nn.BatchNorm1d(256),
            nn.MaxPool1d(kernel_size=2, stride=2),   #256, 73, 120
        )

        # self.decoder = nn.Sequential(
        #     #nn.MaxUnpool1d(kernel_size=2, stride=2),
        #     nn.Dropout(0.25),
        #     nn.ConvTranspose1d(256, 73, 25, stride=2, padding=12, output_padding=1),
        #     #nn.ReLU(True)
        #   )  

    def forward(self, input_):
        latent = self.encoder(input_)
        return latent







class autoencoder_first_16(nn.Module):
    def __init__(self, featureDim):
        super(autoencoder_first_16, self).__init__()
        self.encoder = nn.Sequential(
            nn.Dropout(0.25),
            nn.Conv1d(featureDim,16,5,padding=2),        #256, 73, 200
            nn.ReLU(True),
            nn.MaxPool1d(kernel_size=2, stride=2)   #256, 73, 120
        )
        self.decoder = nn.Sequential(
            #nn.MaxUnpool1d(kernel_size=2, stride=2),
            nn.Dropout(0.25),
            nn.ConvTranspose1d(16, featureDim, 5, stride=2, padding=2, output_padding=1),
            #nn.ReLU(True)
          )  

    def forward(self, x):
        x = self.encoder(x)
        x = self.decoder(x)
        return x




class regressor_fcn_bn_encoder_16(nn.Module):
    def __init__(self):
        super(regressor_fcn_bn_encoder_16, self).__init__()

        self.encoder = nn.Sequential(
            #nn.Dropout(0.25),
            nn.Conv1d(10,16,5,padding=2),        #256, 73, 200
            nn.ReLU(),
            nn.BatchNorm1d(16),

            #nn.Dropout(0.25),
            nn.Conv1d(16,16,5,padding=2),        #256, 73, 200
            #nn.ReLU(),
            nn.BatchNorm1d(16),
            nn.MaxPool1d(kernel_size=2, stride=2),   #256, 73, 120
        )

        # self.decoder = nn.Sequential(
        #     #nn.MaxUnpool1d(kernel_size=2, stride=2),
        #     nn.Dropout(0.25),
        #     nn.ConvTranspose1d(256, 73, 25, stride=2, padding=12, output_padding=1),
        #     #nn.ReLU(True)
        #   )  

    def forward(self, input_):
        latent = self.encoder(input_)
        return latent




class regressor_fcn_bn_encoder_64(nn.Module):
    def __init__(self):
        super(regressor_fcn_bn_encoder_64, self).__init__()

        self.encoder = nn.Sequential(
            #nn.Dropout(0.25),
            nn.Conv1d(10,32,5,padding=2),        #256, 73, 200
            nn.ReLU(),
            nn.BatchNorm1d(32),

            #nn.Dropout(0.25),
            nn.Conv1d(32,64,5,padding=2),        #256, 73, 200
            #nn.ReLU(),
            nn.BatchNorm1d(64),

            #nn.Dropout(0.25),
            nn.Conv1d(64,16,5,padding=2),        #256, 73, 200
            #nn.ReLU(),
            nn.BatchNorm1d(16),
            nn.MaxPool1d(kernel_size=2, stride=2),   #256, 73, 120
        )

        # self.decoder = nn.Sequential(
        #     #nn.MaxUnpool1d(kernel_size=2, stride=2),
        #     nn.Dropout(0.25),
        #     nn.ConvTranspose1d(256, 73, 25, stride=2, padding=12, output_padding=1),
        #     #nn.ReLU(True)
        #   )  

    def forward(self, input_):
        latent = self.encoder(input_)
        return latent
