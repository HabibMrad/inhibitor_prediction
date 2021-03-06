import os
import shutil
import torch

STATS_FILE = "best_stats.txt"
BEST_FILE = "model_best.pth.tar"

def load_model(exp_dir, exp_name, model, optimizer, mode = 'checkpoint', lr = None):
    if mode == 'checkpoint':
        filename = 'checkpoint.pth.tar'
    elif mode == 'best':
        filename = 'model_best.pth.tar'
        
    filepath = os.path.join(exp_dir, exp_name, filename)
    if os.path.isfile(filepath):
        print("=> loading checkpoint '{}'".format(filepath))
        checkpoint = torch.load(filepath)
        epoch = checkpoint['epoch']
        model.load_state_dict(checkpoint['state_dict'])
        for param_group in optimizer.param_groups:
            print ("lr = ", param_group['lr'])
            if lr is not None:
                param_group['lr'] = lr
        optimizer.load_state_dict(checkpoint['optimizer'])

        print("=> loaded checkpoint '{}' (epoch {})"
              .format(filepath, checkpoint['epoch']))
        
        return epoch
    else:
        print("=> no checkpoint found at '{}'".format(filepath))
        return None

    
def save_model(state, loss, exp_dir, exp_name, filename='checkpoint.pth.tar'):
    file_path = os.path.join(exp_dir, exp_name)
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    
    torch.save(state, os.path.join(file_path, filename))
    print ("saved checkpoint to ", file_path)
    best_stats_file = os.path.join(file_path, STATS_FILE)
    if os.path.isfile(best_stats_file):
        with open(best_stats_file, 'r') as best_file:
            best_loss = best_file.read()
        if float(best_loss) > loss:
            shutil.copyfile(os.path.join(file_path, filename), os.path.join(file_path, BEST_FILE))
            print ("best checkpoint! saved to ", BEST_FILE)
            with open(best_stats_file, 'w') as best_file:
                best_file.write("%f"%(loss))
    else:
        shutil.copyfile(os.path.join(file_path, filename), os.path.join(file_path, BEST_FILE))
        print ("best checkpoint! saved to ", BEST_FILE)
        with open(best_stats_file, 'w') as best_file:
            best_file.write("%f"%(loss))