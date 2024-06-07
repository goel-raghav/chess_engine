import torch


def loss_fn(output, target, lambda_):
    eval_target = torch.reshape(target[:,0], (-1, 1))
    result_target = torch.reshape(target[:,1], (-1, 1))

    eval_loss = torch.mean((output - eval_target) ** 2)
    result_loss = torch.mean((output - result_target) ** 2)
    loss = lambda_ * eval_loss + (1 - lambda_) * result_loss
    return eval_loss

if __name__ == "__main__":
    x = torch.tensor([.5, .8, .3])
    y = torch.tensor([[.1, 1], [.1, 1], [.1, 1]])
    print(x)
    print(y)
    print(loss_fn(torch.tensor(x, y, 1)))