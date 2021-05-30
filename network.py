import torch

def add_tensor_1d(x, y):
    s1 = (y.shape[-1] - x.shape[-1]) // 2
    e1 = s1 + x.shape[-1]
    y = y[..., s1:e1]
    if x.shape[1] > y.shape[1]:
        d = [int(i) for i in y.shape]
        d[1] = int(x.shape[1] - y.shape[1])
        y = torch.cat((y, torch.zeros(d, dtype=y.dtype, device=y.device)), -3)

    return x + y

def torch_nanmean_var(x, dim=None, keepdim=True):
    pos = torch.isnan(x) == False
    y = torch.where(pos, x, torch.zeros_like(x))
    d = pos.sum(dim, keepdim=keepdim)
    m = y.sum(dim, keepdim=keepdim) / d
    v = (y ** 2).sum(dim, keepdim=keepdim) / d - (m ** 2)
    return m, v

class GroupNanNorm(torch.nn.Module):
    def __init__(self, num_groups: int, num_channels: int, eps: float = 1e-5, affine: bool = True) -> None:
        super(GroupNanNorm, self).__init__()
        self.num_groups = num_groups
        self.num_channels = num_channels
        self.eps = eps
        self.affine = affine
        if self.affine:
            self.weight = torch.nn.Parameter(torch.Tensor(num_channels))
            self.bias = torch.nn.Parameter(torch.Tensor(num_channels))
        else:
            self.register_parameter('weight', None)
            self.register_parameter('bias', None)
        self.reset_parameters()
        assert (self.num_channels % self.num_groups) == 0

    def reset_parameters(self) -> None:
        if self.affine:
            torch.nn.modules.normalization.init.ones_(self.weight)
            torch.nn.modules.normalization.init.zeros_(self.bias)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        shape = x.shape
        assert shape[1] == self.num_channels

        x = x.view((int(shape[0]), self.num_groups, int(shape[1]) // self.num_groups, -1))
        m, v = torch_nanmean_var(x, (-2, -1), keepdim=True)
        x = (x - m) * torch.rsqrt(v + self.eps)
        x = x.view((int(shape[0]), int(shape[1]), -1))
        if self.affine:
            x = x * self.weight[None, :, None] + self.bias[None, :, None]
        x = x.view(shape)
        return x

    def extra_repr(self) -> str:
        return '{num_groups}, {num_channels}, eps={eps}, ' \
               'affine={affine}'.format(**self.__dict__)

class ResidialBlock1D(torch.nn.Module):
    def __init__(self, input_size, output_size, kernel_size, group_size=16, stride=1,
                 padding=0, dilation=1, residue=True, negative_slope=0.02, nangroup=True):
        super(ResidialBlock1D, self).__init__()
        self.residue = residue
        self.conv = torch.nn.Conv1d(input_size, output_size, kernel_size, stride=stride, padding=padding, dilation=dilation, bias=True)
        if nangroup:
            self.norm = GroupNanNorm(num_groups=output_size // group_size, num_channels=output_size, affine=True)
        else:
            self.norm = torch.nn.GroupNorm(num_groups=output_size // group_size, num_channels=output_size, affine=True)
            
        self.act  = torch.nn.LeakyReLU(negative_slope)

    def forward(self, x):
        y = self.norm(self.conv(x))
        if self.residue:
            y = add_tensor_1d(y, x)
        return self.act(y)

def DeepNetwork1D(input_size=62, output_size=128, hidden_size=512,
                 kernels  =[1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
                 dilations=[1, 1, 1, 1, 2, 2, 2, 4, 4, 4, 4],
                 last_act=False, flag_residue_first=False, nangroup=True):
    
    list_module = list()
    for index in range(len(dilations)-1):
        block_input_size = input_size if index == 0 else hidden_size
        block_dilation   = dilations[index]
        block_kernel     = kernels[index]
        block_residue    = flag_residue_first if index == 0 else True
        module = ResidialBlock1D(block_input_size, hidden_size, kernel_size=block_kernel, group_size=16, stride=1,
            padding=0, dilation=block_dilation, residue=block_residue, negative_slope=0.02, nangroup=nangroup)
        list_module.append(module)
    
    
    block_dilation = dilations[-1]
    block_kernel = kernels[-1]
    if last_act:
        module = ResidialBlock1D(hidden_size, output_size, kernel_size=block_kernel, group_size=16, stride=1,
            padding=0, dilation=block_dilation, residue=False, negative_slope=0.02, nangroup=nangroup)
        list_module.append(module)
    else:
        module = torch.nn.Conv1d(hidden_size, output_size, block_kernel, stride=1, padding=0, dilation=block_dilation, bias=True)
        list_module.append(module)
    
    return torch.nn.Sequential(*list_module)


class IDreveal():
    def __init__(self, time, device='cpu', weights_file='./model.th'):
        self.time = time
        self.device = device
        self.network = DeepNetwork1D(62, 128, 512,
                 kernels  =[1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
                 dilations=[1, 1, 1, 1, 2, 2, 2, 4, 4, 4, 4],
                 last_act=False, flag_residue_first=False, nangroup=True).to(device)
        
        dat = torch.load(weights_file, map_location=self.device)
        
        self.norm = dat['norm']
        self.network.load_state_dict(dat['network'])
        self.network.eval()
        
    def __call__(self, data, stride=1):
        with torch.no_grad():
            time = self.time
            htime = (time-50)//2
            data = torch.from_numpy(data)/self.norm
            data = data.unfold(0, time, stride)
            assert data.shape[1]==62
            assert data.shape[2]==time
            data = torch.split(data, 512, dim=0)
            data = [self.network(x.to(self.device))[:,:,htime].cpu() for x in data]
            data = torch.cat(data,0).numpy()
            
        return data
    