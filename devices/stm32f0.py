from mempoke import MMPeripheral, T


class RCC(MMPeripheral):
    fields = [(T.uint32_t, 'CR'),
              (T.uint32_t, 'CFGR'),
              (T.uint32_t, 'CIR'),
              (T.uint32_t, 'APB2RSTR'),
              (T.uint32_t, 'APB1RSTR'),
              (T.uint32_t, 'AHBENR'),
              (T.uint32_t, 'APB2ENR'),
              (T.uint32_t, 'APB1ENR'),
              (T.uint32_t, 'BDCR'),
              (T.uint32_t, 'CSR'),
              (T.uint32_t, 'AHBRSTR'),
              (T.uint32_t, 'CFGR2'),
              (T.uint32_t, 'CFGR3'),
              (T.uint32_t, 'CR2')]
