import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
import matplotlib.pyplot as plt


class CustomCNN(nn.Module):
    def __init__(
        self,
        input_shape=(3, 64, 64),  # 입력 이미지 크기(채널, 높이, 너비)
        num_classes=10,  # 출력 클래스 수
        depth=2,  # Conv 블록 개수 (예: 2->경량, 4->고성능(더 깊어짐))
        base_channels=32,  # 첫 Conv 블록의 출력 채널 수
        activation="relu",  # 활성화 함수 선택(relu, gelu, leaky_relu, sigmoid, 등)
        kernel_size=3,  # Conv 필터 크기
        dropout_rate=0.25,  # Conv 블록 내 Dropout 비율
        padding="same",  # 패딩 모드 : same, valid, 정수 등
        use_batchnorm=False,  # 배치 정규화 사용 여부
    ):
        super(CustomCNN, self).__init__()

        # 활성화 함수 매핑 (클래스 기반)
        activation_map = {
            "relu": nn.ReLU,
            "leaky_relu": nn.LeakyReLU,
            "gelu": nn.GELU,
            "tanh": nn.Tanh,
            "sigmoid": nn.Sigmoid,
        }

        if activation not in activation_map:
            raise ValueError(
                f"Unsupported activation : {activation}. Choose from {list(activation_map.keys())}"
            )
        self.activation_cls = activation_map[activation]

        self.pool = nn.MaxPool2d(2, 2)  #

        layers = []
        in_channels = input_shape[0]

        for i in range(depth):
            out_channels = base_channels * (2**i)
            #
            pad = self.resolve_padding(padding, kernel_size)

            # 첫 번째 Conv block
            layers.append(
                nn.Conv2d(
                    in_channels, out_channels, kernel_size=kernel_size, padding=pad
                )
            )
            if use_batchnorm:
                layers.append(nn.BatchNorm2d(out_channels))
            layers.append(self.activation_cls())

            # 두 번째 ~ Conv block
            if i < depth - 1:
                layers.append(
                    nn.Conv2d(
                        out_channels, out_channels, kernel_size=kernel_size, padding=pad
                    )
                )
                if use_batchnorm:
                    layers.append(nn.BatchNorm2d(out_channels))
                layers.append(self.activation_cls())

            # 풀링 + 드롭아웃
            layers.append(self.pool)
            layers.append(nn.Dropout(dropout_rate))

            in_channels = out_channels

        self.conv_block = nn.Sequential(*layers)

        # Flatten 크기 자동 계산
        with torch.no_grad():
            dummy = torch.zeros(1, *input_shape)
            x = self.conv_block(dummy)
            self.flatten_dim = x.view(1, -1).shape[1]

        # Fully-connected Layer
        self.fc_layers = nn.Sequential(
            nn.Flatten(),
            nn.Linear(self.flatten_dim, 128),
            self.activation_cls(),
            nn.Dropout(0.5),
            nn.Linear(128, num_classes),
        )

    # 패딩 계산 함수
    @staticmethod
    def resolve_padding(padding, kernel_size):
        if isinstance(padding, str):
            if padding.lower() == "same":
                if isinstance(kernel_size, int):
                    return kernel_size // 2
                elif isinstance(kernel_size, tuple):
                    return tuple(k // 2 for k in kernel_size)
            elif padding.lower() == "valid":
                return 0
            else:
                raise ValueError(f"Unsupported padding String : {padding}")
        elif isinstance(padding, int):
            return padding
        elif isinstance(padding, tuple):
            return padding
        else:
            raise ValueError(f"Unsupported padding type : {type(padding)}")

    # /패딩 계산 함수

    def forward(self, x):
        x = self.conv_block(x)
        x = self.fc_layers(x)
        return x
