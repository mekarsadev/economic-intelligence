import torch.nn as nn


# Membangun model LSTM
class LSTMModel(nn.Module):
    def __init__(self, input_size, hidden_sizes, output_size):
        super(LSTMModel, self).__init__()
        self.hidden_sizes = hidden_sizes
        self.num_layers = len(hidden_sizes)

        self.lstms = nn.ModuleList()
        self.lstms.append(nn.LSTM(input_size, hidden_sizes[0]))

        for i in range(1, self.num_layers):
            self.lstms.append(nn.LSTM(hidden_sizes[i - 1], hidden_sizes[i]))

        self.fc = nn.Linear(hidden_sizes[-1], output_size)
        self.init_weights()

    def init_weights(self):
        for i in range(self.num_layers):
            for name, param in self.lstms[i].named_parameters():
                if "weight" in name:
                    if param.data.dim() > 1:
                        nn.init.xavier_normal_(param)
                    else:
                        nn.init.zeros_(param)
                elif "bias" in name:
                    nn.init.constant_(param, 0)

    def forward(self, input):
        for i in range(self.num_layers):
            output, _ = self.lstms[i](input)
            input = output

        output = self.fc(output[:, -1, :])
        return output
