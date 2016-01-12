from mempoke import MMPeripheral, T


class RCC(MMPeripheral):
    fields = [(T.uint32_t,  'CR'),
              (T.uint32_t,  'CFGR'),
              (T.uint32_t,  'CIR'),
              (T.uint32_t,  'APB2RSTR'),
              (T.uint32_t,  'APB1RSTR'),
              (T.uint32_t,  'AHBENR'),
              (T.uint32_t,  'APB2ENR'),
              (T.uint32_t,  'APB1ENR'),
              (T.uint32_t,  'BDCR'),
              (T.uint32_t,  'CSR'),
              (T.uint32_t,  'AHBRSTR'),
              (T.uint32_t,  'CFGR2'),
              (T.uint32_t,  'CFGR3'),
              (T.uint32_t,  'CR2')]

    AHBENR_bits = {'TSCEN': 24,
                   'IOPFEN': 22,
                   'IOPEEN': 21,
                   'IOPDEN': 20,
                   'IOPCEN': 19,
                   'IOPBEN': 18,
                   'IOPAEN': 17,
                   'CRCEN': 6,
                   'FLITFEN': 4,
                   'SRAMEN': 2,
                   'DMAEN': 0}

    AHBRSTR_bits = {'TSCRST': 24,
                    'IOPFRST': 22,
                    'IOPERST': 21,
                    'IOPDRST': 20,
                    'IOPCRST': 19,
                    'IOPBRST': 18,
                    'IOPARST': 17}


class GPIO(MMPeripheral):
    fields = [(T.uint32_t,  'MODER'),
              (T.uint16_t,  'OTYPER'),
              (T.uint16_t,  None),
              (T.uint32_t,  'OSPEEDR'),
              (T.uint32_t,  'PUPDR'),
              (T.uint16_t,  'IDR'),
              (T.uint16_t,  None),
              (T.uint16_t,  'ODR'),
              (T.uint16_t,  None),
              (T.uint32_t,  'BSRR'),
              (T.uint32_t,  'LCKR'),
              (T.uint32_t,  'AFR0'),
              (T.uint32_t,  'AFR1'),
              (T.uint16_t,  'BRR'),
              (T.uint16_t,  None)]

    MODE_bits = {'INPUT': 0x0,
                 'OUTPUT': 0x1,
                 'ANALOG': 0x3,
                 'ALT': 0x2}

    OTYPE_bits = {'PUSHPULL': 0,
                  'OPENDRAIN': 1}

    PUPD_bits = {'NONE': 0,
                 'UP': 1,
                 'DOWN': 2}

    OSPEED_bits = {'2MHz': 0x0,
                   '10MHz': 0x1,
                   '50MHz': 0x3}


class ADC(MMPeripheral):
    fields = [(T.uint32_t,  'ISR'),
              (T.uint32_t,  'IER'),
              (T.uint32_t,  'CR'),
              (T.uint32_t,  'CFGR1'),
              (T.uint32_t,  'CFGR2'),
              (T.uint32_t,  'SMPR'),
              (T.uint32_t,  None),
              (T.uint32_t,  None),
              (T.uint16_t,  'TR_LT'),
              (T.uint16_t,  'TR_HT'),
              (T.uint32_t,  None),
              (T.uint32_t,  'CHSELR'),
              (T.uint32_t,  None),
              (T.uint32_t,  None),
              (T.uint32_t,  None),
              (T.uint32_t,  None),
              (T.uint32_t,  None),
              (T.uint16_t,  'DR_DATA'),
              (T.uint16_t,  None)]

    ISR_bits = {'AWD': 7,
                'OVR': 4,
                'EOSEQ': 3,
                'EOC': 2,
                'EOSMP': 1,
                'ADRDY': 0}

    IER_bits = {'AWDIE': 7,
                'OVRIE': 4,
                'EOSEQIE': 3,
                'EOCIE': 2,
                'EOSMPIE': 1,
                'ADRDYIE': 0}

    CR_bits = {'ADCAL': 31,
               'ADSTP': 4,
               'ADSTART': 2,
               'ADDIS': 1,
               'ADEN': 0}

    CFGR1_bits = {'AWDEN': 23,
                  'AWDSGL': 22,
                  'DISCEN': 16,
                  'AUTOFF': 15,
                  'WAIT': 14,
                  'CONT': 13,
                  'OVRMOD': 12,
                  'ALIGN': 5,
                  'SCANDIR': 2,
                  'DMACFG': 1,
                  'DMAEN': 0}


class DAC(MMPeripheral):
    fields = [(T.uint32_t,  'CR'),
              (T.uint32_t,  'SWTRIGR'),
              (T.uint32_t,  'DHR12R1'),
              (T.uint32_t,  'DHR12L1'),
              (T.uint8_t,  'DHR8R1'),
              (T.uint8_t,  None),
              (T.uint16_t,  None),
              (T.uint32_t,  'DHR12R2'),
              (T.uint32_t,  'DHR12L2'),
              (T.uint8_t,  'DHR8R2'),
              (T.uint8_t,  None),
              (T.uint16_t,  None),
              (T.uint32_t,  'DHR12RD'),
              (T.uint32_t,  'DHR12LD'),
              (T.uint32_t,  'DOR1'),
              (T.uint32_t,  'DOR2'),
              (T.uint32_t,  'SR')]

    CR_bits = {'DMAUDRIE2': 29,
               'DMAEN2': 28,
               'TEN2': 18,
               'BOFF2': 17,
               'EN2': 16,
               'DMAUDRIE1': 13,
               'DMAEN1': 12,
               'TEN1': 2,
               'BOFF1': 1,
               'EN1': 0}

    SWTRIGR_bits = {'SWTRIG2': 1,
                    'SWTRIG1': 0}

    SR_bits = {'DMAUDR2': 29,
               'DMAUDR1': 13}


class USART(MMPeripheral):
    fields = [(T.uint32_t,  'CR1'),
              (T.uint32_t,  'CR2'),
              (T.uint32_t,  'CR3'),
              (T.uint32_t,  'BRR'),
              (T.uint16_t,  'GTPR'),
              (T.uint16_t,  None),
              (T.uint32_t,  'RTOR'),
              (T.uint32_t,  'RQR'),
              (T.uint32_t,  'ISR'),
              (T.uint32_t,  'ICR'),
              (T.uint8_t,  'RDR'),
              (T.uint8_t,  None),
              (T.uint16_t,  None),
              (T.uint8_t,  'TDR'),
              (T.uint8_t,  None),
              (T.uint16_t,  None)]

    CR1_bits = {'M1': 28,
                'EOBIE': 27,
                'RTOIE': 26,
                'DEAT4': 25,
                'DEAT3': 24,
                'DEAT2': 23,
                'DEAT1': 22,
                'DEAT0': 21,
                'DEDT4': 20,
                'DEDT3': 19,
                'DEDT2': 18,
                'DEDT1': 17,
                'DEDT0': 16,
                'OVER8': 15,
                'CMIE': 14,
                'MME': 13,
                'M0': 12,
                'WAKE': 11,
                'PCE': 10,
                'PS': 9,
                'PEIE': 8,
                'TXEIE': 7,
                'TCIE': 6,
                'RXNEIE': 5,
                'IDLEIE': 4,
                'TE': 3,
                'RE': 2,
                'UE': 0}

    CR2_bits = {'RTOEN': 23,
                'ABRMOD1': 22,
                'ABRMOD0': 21,
                'ABREN': 20,
                'MSBFIRST': 19,
                'DATAINV': 18,
                'TXINV': 17,
                'RXINV': 16,
                'SWAP': 15,
                'LINEN': 14,
                'CLKEN': 11,
                'CPOL': 10,
                'CPHA': 9,
                'LBCL': 8,
                'LBDIE': 6,
                'LBDL': 5,
                'ADDM7': 4}

    CR3_bits = {'WUFIE': 22,
                'DEP': 15,
                'DEM': 14,
                'DDRE': 13,
                'OVRDIS': 12,
                'ONEBIT': 11,
                'CTSIE': 10,
                'CTSE': 9,
                'RTSE': 8,
                'DMAT': 7,
                'DMAR': 6,
                'SCEN': 5,
                'NACK': 4,
                'HDSEL': 3,
                'IRLP': 2,
                'IREN': 1,
                'EIE': 0}

    RQR_bits = {'TXFRQ': 4,
                'RXFRQ': 3,
                'MMRQ': 2,
                'SBKRQ': 1,
                'ABRRQ': 0}

    ISR_bits = {'REACK': 22,
                'TEACK': 21,
                'WUF': 20,
                'RWU': 19,
                'SBKF': 18,
                'CMF': 17,
                'BUSY': 16,
                'ABRF': 15,
                'ABRE': 14,
                'EOBF': 12,
                'RTOF': 11,
                'CTS': 10,
                'CTSIF': 9,
                'LBDF': 8,
                'TXE': 7,
                'TC': 6,
                'RXNE': 5,
                'IDLE': 4,
                'ORE': 3,
                'NF': 2,
                'FE': 1,
                'PE': 0}

    ICR_bits = {'WUCF': 20,
                'CMCF': 17,
                'EOBCF': 12,
                'RTOCF': 11,
                'CTSCF': 9,
                'LBDCF': 8,
                'TCCF': 6,
                'IDLECF': 4,
                'ORECF': 3,
                'NCF': 2,
                'FECF': 1,
                'PECF': 0}


class SPI(MMPeripheral):
    fields = [(T.uint32_t,  'CR1'),
              (T.uint32_t,  'CR2'),
              (T.uint32_t,  'SR'),
              (T.uint16_t,  'DR'),
              (T.uint16_t,  None),
              (T.uint16_t,  'CRCPR'),
              (T.uint16_t,  None),
              (T.uint16_t,  'RXCRCR'),
              (T.uint16_t,  None),
              (T.uint16_t,  'TXCRCR'),
              (T.uint16_t,  None),
              (T.uint32_t,  'I2SCFGR'),
              (T.uint32_t,  'I2SPR')]

    CR1_bits = {'BIDIMODE': 15,
                'BIDIOE': 14,
                'CRCEN': 13,
                'CRCNEXT': 12,
                'CRCL': 11,
                'RXONLY': 10,
                'SSM': 9,
                'SSI': 8,
                'LSBFIRST': 7,
                'SPE': 6,
                'MSTR': 2,
                'CPOL': 1,
                'CPHA': 0}

    CR2_bits = {'LDMA_TX': 14,
                'LDMA_RX': 13,
                'FRXTH': 12,
                'TXEIE': 7,
                'RXNEIE': 6,
                'ERRIE': 5,
                'FRF': 4,
                'NSSP': 3,
                'SSOE': 2,
                'TXDMAEN': 1,
                'RXDMAEN': 0}

    SR_bits = {'FRE': 8,
               'BSY': 7,
               'OVR': 6,
               'MODF': 5,
               'CRCERR': 4,
               'UDR': 3,
               'CHSIDE': 2,
               'TXE': 1,
               'RXNE': 0}

    I2SCFGR_bits = {'I2SMOD': 11,
                    'I2SE': 10,
                    'PCMSYNC': 7,
                    'CKPOL': 3,
                    'CHLEN': 0}

    I2SPR_bits = {'MCKOE': 9,
                  'ODD': 8}


class USB(MMPeripheral):
    fields = [(T.uint16_t,  'EP0R'),
              (T.uint16_t,  None),
              (T.uint16_t,  'EP1R'),
              (T.uint16_t,  None),
              (T.uint16_t,  'EP2R'),
              (T.uint16_t,  None),
              (T.uint16_t,  'EP3R'),
              (T.uint16_t,  None),
              (T.uint16_t,  'EP4R'),
              (T.uint16_t,  None),
              (T.uint16_t,  'EP5R'),
              (T.uint16_t,  None),
              (T.uint16_t,  'EP6R'),
              (T.uint16_t,  None),
              (T.uint16_t,  'EP7R'),
              (T.uint16_t,  None),
              (T.uint64_t,  None),
              (T.uint64_t,  None),
              (T.uint64_t,  None),
              (T.uint64_t,  None),
              (T.uint16_t,  'CNTR'),
              (T.uint16_t,  None),
              (T.uint16_t,  'ISTR'),
              (T.uint16_t,  None),
              (T.uint16_t,  'FNR'),
              (T.uint16_t,  None),
              (T.uint16_t,  'DADDR'),
              (T.uint16_t,  None),
              (T.uint16_t,  'BTABLE'),
              (T.uint16_t,  None),
              (T.uint16_t,  'LPMCSR'),
              (T.uint16_t,  None),
              (T.uint16_t,  'BCDR'),
              (T.uint16_t,  None)]

    EPxR_bits = {'CTR_RX': 15,
                 'DTOG_RX': 14,
                 'SETUP': 11,
                 'EP_KIND': 8,
                 'CTR_TX': 7,
                 'DTOG_TX': 6}

    CNTR_bits = {'CTRM': 15,
                 'PMAOVRM': 14,
                 'ERRM': 13,
                 'WKUPM': 12,
                 'SUSPM': 11,
                 'RESETM': 10,
                 'SOFM': 9,
                 'ESOFM': 8,
                 'L1REQM': 7,
                 'L1RESUME': 5,
                 'RESUME': 4,
                 'FSUSP': 3,
                 'LPMODE': 2,
                 'PDWN': 1,
                 'FRES': 0}

    ISTR_bits = {'CTR': 15,
                 'PMAOVR': 14,
                 'ERR': 13,
                 'WKUP': 12,
                 'SUSP': 11,
                 'RESET': 10,
                 'SOF': 9,
                 'ESOF': 8,
                 'L1REQ': 7,
                 'DIR': 4}

    FNR_bits = {'RXDP': 15,
                'RXDM': 14,
                'LCK': 13}

    DADDR_bits = {'EF': 7}

    LPMCSR_bits = {'REMWAKE': 3,
                   'LPMACK': 1,
                   'LPMEN': 0}

    BCDR_bits = {'DPPU': 15,
                 'PS2DET': 7,
                 'SDET': 6,
                 'PDET': 5,
                 'DCDET': 4,
                 'SDEN': 3,
                 'PDEN': 2,
                 'DCDEN': 1,
                 'BCDEN': 0}


class STM32F0(object):

    PERIPHERALS_BASE = 0x40000000

    APB_BUS_BASE = PERIPHERALS_BASE
    AHB1_BUS_BASE = PERIPHERALS_BASE + 0x00020000
    AHB2_BUS_BASE = PERIPHERALS_BASE + 0x08000000

    def __init__(self, device_memory):
        self.GPIO = {'A': GPIO(self.AHB2_BUS_BASE + 0x00000000, device_memory),
                     'B': GPIO(self.AHB2_BUS_BASE + 0x00000400, device_memory),
                     'C': GPIO(self.AHB2_BUS_BASE + 0x00000800, device_memory),
                     'D': GPIO(self.AHB2_BUS_BASE + 0x00000C00, device_memory),
                     'E': GPIO(self.AHB2_BUS_BASE + 0x00001000, device_memory),
                     'F': GPIO(self.AHB2_BUS_BASE + 0x00001400, device_memory)}
        self.RCC = RCC(self.AHB1_BUS_BASE + 0x00001000, device_memory)
        self.USART = {1: USART(self.APB_BUS_BASE + 0x00013800, device_memory),
                      8: USART(self.APB_BUS_BASE + 0x00011C00, device_memory),
                      7: USART(self.APB_BUS_BASE + 0x00011800, device_memory),
                      6: USART(self.APB_BUS_BASE + 0x00011400, device_memory),
                      5: USART(self.APB_BUS_BASE + 0x00005000, device_memory),
                      4: USART(self.APB_BUS_BASE + 0x00004C00, device_memory),
                      3: USART(self.APB_BUS_BASE + 0x00004800, device_memory),
                      2: USART(self.APB_BUS_BASE + 0x00004000, device_memory)}
        self.ADC = ADC(self.APB_BUS_BASE + 0x00012400, device_memory)
        self.DAC = DAC(self.APB_BUS_BASE + 0x00007800, device_memory)
        self.USB = USB(self.APB_BUS_BASE + 0x00005C00, device_memory)
        self.SPI = {2: SPI(self.APB_BUS_BASE + 0x00003800, device_memory)}
