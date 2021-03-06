import argparse
import logging

import torch
import torch.nn.functional as F
import torchvision
from torch.autograd import Variable
import numpy as np
import dataset
import ndf
from sklearn import metrics
# import ignite
# from ignite import metrics


def parse_arg():
    logging.basicConfig(
        level=logging.WARNING,
        format="[%(asctime)s]: %(levelname)s: %(message)s"
    )
    parser = argparse.ArgumentParser(description='train.py')
    parser.add_argument('-dataset', choices=['mnist', 'adult', 'letter', 'yeast','gisette','arrhythmia','cardiotocography','breastcancer','nomao','mutiplefeatures','isolet5','madelon','secom'], default='mnist')
    parser.add_argument('-batch_size', type=int, default=128)

    parser.add_argument('-feat_dropout', type=float, default=0.5)

    parser.add_argument('-n_tree', type=int, default=10)
    parser.add_argument('-tree_depth', type=int, default=10)
    parser.add_argument('-n_class', type=int, default=10)
    parser.add_argument('-tree_feature_rate', type=float, default=0.5)

    parser.add_argument('-lr', type=float, default=0.001, help="sgd: 10, adam: 0.001")
    parser.add_argument('-gpuid', type=int, default=-1)
    parser.add_argument('-jointly_training', action='store_true', default=False)
    parser.add_argument('-epochs', type=int, default=10)
    parser.add_argument('-report_every', type=int, default=10)

    opt = parser.parse_args()
    return opt


def prepare_db(opt):
    print("Use %s dataset" % (opt.dataset))

    if opt.dataset == 'mnist':
        train_dataset = torchvision.datasets.MNIST('./data/mnist', train=True, download=True,
                                                   transform=torchvision.transforms.Compose([
                                                       torchvision.transforms.ToTensor(),
                                                       torchvision.transforms.Normalize((0.1307,), (0.3081,))
                                                   ]))

        eval_dataset = torchvision.datasets.MNIST('./data/mnist', train=False, download=True,
                                                  transform=torchvision.transforms.Compose([
                                                      torchvision.transforms.ToTensor(),
                                                      torchvision.transforms.Normalize((0.1307,), (0.3081,))
                                                  ]))
        return {'train': train_dataset, 'eval': eval_dataset}

    elif opt.dataset == 'adult':
        train_dataset = dataset.UCIAdult('./data/uci_adult', train=True)
        eval_dataset = dataset.UCIAdult('./data/uci_adult', train=False)
        return {'train': train_dataset, 'eval': eval_dataset}

    elif opt.dataset == 'letter':
        train_dataset = dataset.UCILetter('./data/uci_letter', train=True)
        eval_dataset = dataset.UCILetter('./data/uci_letter', train=False)
        return {'train': train_dataset, 'eval': eval_dataset}

    elif opt.dataset == 'yeast':
        train_dataset = dataset.UCIYeast('./data/uci_yeast', train=True)
        eval_dataset = dataset.UCIYeast('./data/uci_yeast', train=False)
        return {'train': train_dataset, 'eval': eval_dataset}
    elif opt.dataset == 'gisette':
        train_dataset = dataset.UCIGisette('./data/uci_gisette', train=True)
        eval_dataset = dataset.UCIGisette('./data/uci_gisette', train=False)
        return {'train': train_dataset, 'eval': eval_dataset}
    elif opt.dataset == 'arrhythmia':
        train_dataset = dataset.UCIArrhythmia('./data/uci_arrhythmia', train=True)
        eval_dataset = dataset.UCIArrhythmia('./data/uci_arrhythmia', train=False)
        return {'train': train_dataset, 'eval': eval_dataset}
    elif opt.dataset == 'cardiotocography':
        train_dataset = dataset.UCICardiotocography('./data/uci_card', train=True)
        eval_dataset = dataset.UCICardiotocography('./data/uci_card', train=False)
        return {'train': train_dataset, 'eval': eval_dataset}
    elif opt.dataset == 'breastcancer':
        train_dataset = dataset.UCIBreastcancer('./data/uci_breast', train=True)
        eval_dataset = dataset.UCIBreastcancer('./data/uci_breast', train=False)
        return {'train': train_dataset, 'eval': eval_dataset}
    elif opt.dataset == 'nomao':
        train_dataset = dataset.UCINomao('./data/uci_nomao', train=True)
        eval_dataset = dataset.UCINomao('./data/uci_nomao', train=False)
        return {'train': train_dataset, 'eval': eval_dataset}
    elif opt.dataset == 'multiplefeatures':
        train_dataset = dataset.UCIMultiplefeatures('./data/uci_multiple_features', train=True)
        eval_dataset = dataset.UCIMultiplefeatures('./data/uci_multiple_features', train=False)
        return {'train': train_dataset, 'eval': eval_dataset}
    elif opt.dataset == 'madelon':
        train_dataset = dataset.UCIMadelon('./data/uci_madelon', train=True)
        eval_dataset = dataset.UCIMadelon('./data/uci_madelon', train=False)
        return {'train': train_dataset, 'eval': eval_dataset}
    elif opt.dataset == 'secom':
        train_dataset = dataset.UCISecom('./data/uci_secom', train=True)
        eval_dataset = dataset.UCISecom('./data/uci_secom', train=False)
        return {'train': train_dataset, 'eval': eval_dataset}
    elif opt.dataset == 'isolet5':
        train_dataset = dataset.UCIIsolet5('./data/uci_isolet5', train=True)
        eval_dataset = dataset.UCIIsolet5('./data/uci_isolet5', train=False)
        return {'train': train_dataset, 'eval': eval_dataset}
    
    else:
        raise NotImplementedError


def prepare_model(opt):
    if opt.dataset == 'mnist':
        feat_layer = ndf.MNISTFeatureLayer(opt.feat_dropout)
    elif opt.dataset == 'adult':
        feat_layer = ndf.UCIAdultFeatureLayer(opt.feat_dropout)
    elif opt.dataset == 'letter':
        feat_layer = ndf.UCILetterFeatureLayer(opt.feat_dropout)
    elif opt.dataset == 'yeast':
        feat_layer = ndf.UCIYeastFeatureLayer(opt.feat_dropout)
    elif opt.dataset == 'gisette':
        feat_layer = ndf.UCIGisetteFeatureLayer(opt.feat_dropout)
    elif opt.dataset == 'arrhythmia':
        feat_layer = ndf.UCIArrhythmiaFeatureLayer(opt.feat_dropout)
    elif opt.dataset == 'cardiotocography':
        feat_layer = ndf.UCICardiotocographyFeatureLayer(opt.feat_dropout)
    elif opt.dataset == 'breastcancer':
        feat_layer = ndf.UCIBreastcancerFeatureLayer(opt.feat_dropout)
    elif opt.dataset == 'nomao':
        feat_layer = ndf.UCINomaoFeatureLayer(opt.feat_dropout)
    elif opt.dataset == 'mutiplefeatures':
        feat_layer = ndf.UCIMutiplefeaturesFeatureLayer(opt.feat_dropout)
    elif opt.dataset == 'madelon':
        feat_layer = ndf.UCIMadelonFeatureLayer(opt.feat_dropout)
    elif opt.dataset == 'secom':
        feat_layer = ndf.UCISecomFeatureLayer(opt.feat_dropout)
    elif opt.dataset == 'isolet5':
        feat_layer = ndf.UCIIsolet5FeatureLayer(opt.feat_dropout)
    
    else:
        raise NotImplementedError

    forest = ndf.Forest(n_tree=opt.n_tree, tree_depth=opt.tree_depth, n_in_feature=feat_layer.get_out_feature_size(),
                        tree_feature_rate=opt.tree_feature_rate, n_class=opt.n_class,
                        jointly_training=opt.jointly_training)
    model = ndf.NeuralDecisionForest(feat_layer, forest)

    if opt.cuda:
        model = model.cuda()
    else:
        model = model.cpu()

    return model


def prepare_optim(model, opt):
    params = [p for p in model.parameters() if p.requires_grad]
    return torch.optim.Adam(params, lr=opt.lr, weight_decay=1e-5)


def train(model, optim, db, opt):
    for epoch in range(1, opt.epochs + 1):
        # Update \Pi
        if not opt.jointly_training:
            print("Epoch %d : Two Stage Learing - Update PI" % (epoch))
            # prepare feats
            cls_onehot = torch.eye(opt.n_class)
            feat_batches = []
            target_batches = []
            train_loader = torch.utils.data.DataLoader(db['train'], batch_size=opt.batch_size, shuffle=True)
            with torch.no_grad():
                for batch_idx, (data, target) in enumerate(train_loader):
                    if opt.cuda:
                        data, target, cls_onehot = data.cuda(), target.long().cuda(), cls_onehot.cuda()
                    data = Variable(data)
                    # Get feats
                    feats = model.feature_layer(data)
                    feats = feats.view(feats.size()[0], -1)
                    feat_batches.append(feats)
#                     target = target.long().cuda()
#                     print(target.type())
                    target_batches.append(cls_onehot[target])
#                     target = target.int().cuda()

                # Update \Pi for each tree
                for tree in model.forest.trees:
                    mu_batches = []
                    for feats in feat_batches:
                        mu = tree(feats)  # [batch_size,n_leaf]
                        mu_batches.append(mu)
                    for _ in range(20):
                        new_pi = torch.zeros((tree.n_leaf, tree.n_class))  # Tensor [n_leaf,n_class]
                        if opt.cuda:
                            new_pi = new_pi.cuda()
                        for mu, target in zip(mu_batches, target_batches):
                            pi = tree.get_pi()  # [n_leaf,n_class]
                            prob = tree.cal_prob(mu, pi)  # [batch_size,n_class]

                            # Variable to Tensor
                            pi = pi.data
                            prob = prob.data
                            mu = mu.data

                            _target = target.unsqueeze(1)  # [batch_size,1,n_class]
                            _pi = pi.unsqueeze(0)  # [1,n_leaf,n_class]
                            _mu = mu.unsqueeze(2)  # [batch_size,n_leaf,1]
                            _prob = torch.clamp(prob.unsqueeze(1), min=1e-6, max=1.)  # [batch_size,1,n_class]

                            _new_pi = torch.mul(torch.mul(_target, _pi), _mu) / _prob  # [batch_size,n_leaf,n_class]
                            new_pi += torch.sum(_new_pi, dim=0)
                        # test
                        # import numpy as np
                        # if np.any(np.isnan(new_pi.cpu().numpy())):
                        #    print(new_pi)
                        # test
                        new_pi = F.softmax(Variable(new_pi), dim=1).data
                        tree.update_pi(new_pi)

        # Update \Theta
        model.train()
        train_loader = torch.utils.data.DataLoader(db['train'], batch_size=opt.batch_size, shuffle=True)
        for batch_idx, (data, target) in enumerate(train_loader):
            if opt.cuda:
                data, target = data.cuda(), target.long().cuda()
            data, target = Variable(data), Variable(target)
            optim.zero_grad()
            output = model(data)
            loss = F.nll_loss(torch.log(output), target)
            loss.backward()
            # torch.nn.utils.clip_grad_norm([ p for p in model.parameters() if p.requires_grad],
            #                              max_norm=5)
            optim.step()
            if batch_idx % opt.report_every == 0:
                print('Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}'.format(
                    epoch, batch_idx * len(data), len(train_loader.dataset),
                           100. * batch_idx / len(train_loader), loss.item()))

        # Eval
        model.eval()
        test_loss = 0
        correct = 0
        test_loader = torch.utils.data.DataLoader(db['eval'], batch_size=opt.batch_size, shuffle=True)
        with torch.no_grad():
            targets = np.array([])
            preds = None
            i = 0
            for data, target in test_loader:
                if opt.cuda:
                    data, target = data.cuda(), target.long().cuda()
                data, target = Variable(data), Variable(target)
                output = model(data)
                targets = np.concatenate((targets, target.cpu().numpy()), axis = 0)
                test_loss += F.nll_loss(torch.log(output), target, size_average=False).item()  # sum up batch loss
                pred = output.data.max(1, keepdim=True)[1]  # get the index of the max log-probability
                if i == 0:
                    preds = output.cpu().numpy()[:]
                    i += 1
                else:
                    preds = np.concatenate((preds, output.cpu().numpy()[:]), axis = 0)
                correct += pred.eq(target.data.view_as(pred)).cpu().sum()

                

            test_loss /= len(test_loader.dataset)
            print('\nTest set: Average loss: {:.4f}, Accuracy: {}/{} ({:.6f})\n'.format(
                test_loss, correct, len(test_loader.dataset),
                correct / len(test_loader.dataset)))
            
            # auc over multiple classes
            if preds.shape[1] > 2:
                newtargets = np.zeros([len(targets),preds.shape[1]])
                for i in range(len(targets)):
                    newtargets[i,int(targets[i])] = 1
                print('auc score:')
#                 print(preds.T.shape)
#                 print(newtargets.T.shape)
                print(metrics.roc_auc_score(newtargets.T, preds.T, average = 'macro', multi_class = 'ovo'))
            else:
                print('auc score:')
                print(metrics.roc_auc_score(targets, preds[:,1]))



def main():
    opt = parse_arg()

    # GPU
    opt.cuda = opt.gpuid >= 0
    if opt.gpuid >= 0:
        torch.cuda.set_device(opt.gpuid)
    else:
        print("WARNING: RUN WITHOUT GPU")

    db = prepare_db(opt)
    model = prepare_model(opt)
    optim = prepare_optim(model, opt)
    train(model, optim, db, opt)


if __name__ == '__main__':
    main()
