import sys
sys.path.append('../../motionsynth_data/motion')
from Pivots import Pivots
from Quaternions import Quaternions

def print_options(parser,opt):
    option_dict = dict()

    message = ''
    message += '----------------- Options ---------------\n'
    for k, v in sorted(vars(opt).items()):
        option_dict[k] = v

        comment = ''
        default = parser.get_default(k)
        if v != default:
            comment = '\t[default: %s]' % str(default)
        message += '{:>25}: {:<30}{}\n'.format(str(k), str(v), comment)
    message += '----------------- End -------------------'
    print(message)

    return message, option_dict

import json
import os
def save_options(checkpoints_dir, message, options_dict):

    # save to the disk
    #expr_dir = os.path.join(checkpoints_dir, 'options.txt')
    #util.mkdirs(expr_dir)
    if not os.path.exists(checkpoints_dir):
        os.makedirs(checkpoints_dir)
    file_name = os.path.join(checkpoints_dir, 'opt.txt')
    with open(file_name, 'wt') as opt_file:
        opt_file.write(message)
        opt_file.write('\n')

    file_name = os.path.join(checkpoints_dir, 'opt.json')
    with open(file_name, 'wt') as opt_file:
        json.dump(options_dict,opt_file)
    


import argparse
def my_args_parser():

    parser = argparse.ArgumentParser(description='VAE MNIST Example')
    parser.add_argument('--epochs', type=int, default=500001, metavar='N',
                        help='number of epochs to train (default: 50001)')

    parser.add_argument('--batch', type=int, default=256, metavar='N',
                        help='batch size (default: 2018)')

    parser.add_argument('--gpu', type=int, default=0, metavar='N',
                        help='Select gpu (default: 0)')

    parser.add_argument('--checkpoint_freq', type=int, default=50, metavar='N',
                        help='How frequently save the checkpoint (default: every 50 epoch)')

    parser.add_argument('--model', type=str, default='speackClass_allSignal',
                        help='a model name in the model_zoo.py (default: regressor_fcn_bn_updated')

    parser.add_argument('--blockmode', type=int, default=0,
                        help='blockmode. block which features in the input (0: no blocking')                         

    parser.add_argument('--solver', type=str, default='adam_ams',
                        help='Optimization solver. adam or sgd, adam_ams. (default: adam_ams')

    parser.add_argument('--db', type=str, default='haggling_socialmodel_wl',
                        help='Database for training cmu...(default: cmu')

    parser.add_argument('--finetune', type=str, default='',
                        help='if a folder is specified, then restart training by loading the last saved model files')

    parser.add_argument('--check_root', type=str, default='./',
                        help='The root dir to make subfolders for the check point (default: ./) ')

    parser.add_argument('--weight_kld', type=float, default='0.1',
                        help='Weight for the KLD term in VAE training (default: 0.1) ')

    parser.add_argument('--autoreg', type=int, default='0',
                        help='If >0, train with autoregressive mode. (using init 150 frames input and later 150 frames as output) (default: 0')

    parser.add_argument('--lstm_hidden_dim', type=int, default='12',
                        help='Hidden layer dimension for LSTM layer (default: 12')
    
    parser.add_argument('--faceParam_feature_dim', type=int, default='200',
                        help='Face Mesh Parameter Feature Dimension used for training (default: 200')
    
    parser.add_argument('--inputSubject', type=int, default='2',
                        help='Input person Idx (default: 2)')
    
    return parser



"""
make a checkpoint folder (try not to overwrite the olde one)
Input:
    - args
    - model: to use the model's name
"""
def setCheckPointFolder(args,model):

    #pretrain_epoch = 0
    if args.finetune =='':
        #pretrain_batch_size =args.batch  #Assume current batch was used in pretraining

        if 'socialmodel' in args.db:
            checkpointFolder = args.check_root + '/social_'+ model.__class__.__name__
        else:
            checkpointFolder = args.check_root + '/'+ model.__class__.__name__
        
        if not os.path.exists(checkpointFolder):
            os.mkdir(checkpointFolder)
        else: #if already exist
            tryIdx =1
            while True:
                newCheckName = checkpointFolder + '_try' + str(tryIdx)
                if not os.path.exists(newCheckName):
                    checkpointFolder = newCheckName
                    os.mkdir(checkpointFolder)
                    break
                else:
                    tryIdx += 1
    else:       #FineTuning
        checkpointFolder = args.check_root+ '/' + args.finetune

    return checkpointFolder


"""

Input:
    - checkpointFolder
    - model: to use the model's name
"""
import torch
def loadPreTrained(args, checkpointFolder, model, optimizer):

    checkpointList =  [os.path.join(checkpointFolder,f) for f in sorted(list(os.listdir(checkpointFolder)))
                if os.path.isfile(os.path.join(checkpointFolder,f))
                    and f.endswith('.pth') ] 

    pretrain_epoch = 0

    #Find Last Epoch
    last_epoch =0
    for name in checkpointList:
        pretrain_epoch= int(name[(name.find('checkpoint_') + 12):-4])
        if last_epoch <pretrain_epoch:
            last_epoch= pretrain_epoch
            trainResultName = name


    #checkpointList.sort(key=lambda x: os.path.getmtime(x))
    #trainResultName =checkpointList[-1]
    pretrain_epoch= int(trainResultName[(trainResultName.find('checkpoint_') + 12):-4])
    pretrain_epoch = pretrain_epoch+1

    try:
        log_file_name = os.path.join(checkpointFolder, 'opt.json')
        with open(log_file_name, 'r') as opt_file:
            options_dict = json.load(opt_file)
        pretrain_batch_size = options_dict['batch']

    except:
        pretrain_batch_size =args.batch  #Assume current batch was used in pretraining
        
    #Fine Last Epoch file
    print('load previous state: {0}'.format(trainResultName))
    model.load_state_dict(torch.load(trainResultName, map_location=lambda storage, loc: storage),strict=False)

    #Checking optimizer file
    trainResultName = trainResultName+'o'
    if os.path.exists(trainResultName):
        print('load previous state: {0}'.format(trainResultName))
        optimizer.load_state_dict(torch.load(trainResultName, map_location=lambda storage, loc: storage))


    return model, optimizer, pretrain_epoch, pretrain_batch_size


import numpy as np
#input 2xframes
#output 3xframes where Yaxis has zeros
def data_2dTo3D(data_2d, newRowIdx =1):
    data_3d = np.zeros((3, data_2d.shape[1])) #(3,frames)

    if newRowIdx==0:
        data_3d[1,:] = data_2d[0,:]
        data_3d[2,:] = data_2d[1,:]
    elif newRowIdx==1:
        data_3d[0,:] = data_2d[0,:]
        data_3d[2,:] = data_2d[1,:]
    else:#elif newRowIdx==2:
        data_3d[0,:] = data_2d[0,:]
        data_3d[1,:] = data_2d[1,:]

    return data_3d


#(numSkel, 66, frames)
def ComputeHeadOrientation(skeletons, faceNormal=None):

    i=12
    neckPt = skeletons[:,(3*i):(3*i+3),:].copy()
    trans = neckPt#skeletons[:,:3,:]

    trans[:,1,:] -=20

    # faceMassCenter = np.array([-0.002735  , -1.44728992,  0.2565446 ])*100
    # faceMassCenter[1] +=20
    # faceMassCenter = faceMassCenter[np.newaxis,:,np.newaxis]
    # trans -=faceMassCenter


    """ Compute Rvelocity"""
    rotation_angle_list = []
    if faceNormal is not None:
        for i in range(len(faceNormal)):

            forward = faceNormal[i] # (2,frames)
            if forward.shape[0]==2:
                forward = data_2dTo3D(forward) # (2,frames)
            forward = np.swapaxes(forward,0,1) #(frames, 3)
            target = np.array([[0,0,1]]).repeat(len(forward), axis=0) #(frames, 3)
            rotation_q = Quaternions.between(target, forward)[:,np.newaxis]    #forward:(frame,3)

            #up = np.array([[0,1,0]]).repeat(len(forward), axis=0) #(frames, 3)
            #down = np.array([[0,-1,0]]).repeat(len(forward), axis=0) #(frames, 3)
            #rotation_q2 = Quaternions.between(up,down)[:,np.newaxis]    #forward:(frame,3)
            #rotation_q = rotation_q2#* rotation_q

            rotation_angle = [rotation_q[i].angle_axis() for i in range(len(rotation_q))]

            rotation_angle = [i[0] * i[1] for i in rotation_angle]
            rotation_angle = np.squeeze(np.array(rotation_angle)) #(frames, 3)
            rotation_angle = np.swapaxes(rotation_angle,0,1) #(3, frames)

            rotation_angle_list.append(rotation_angle)


    #adjust length
    length = min( [ i.shape[1] for i in rotation_angle_list])
    rotation_angle_list = [ f[:,:length] for f in rotation_angle_list ]
    rotation_angle_list = np.array(rotation_angle_list) #(3,3, frames)

    return trans, rotation_angle_list #(numSkel,3, frames)