class Configs(object):

    FILE_DOC: list = ["/**", " * AutoGen", " */"]

    Base_Type = {
        'int': 1,
        'String': 1,
        'long': 1,
        'Boolean': 1,
        'Byte': 1
    }

    MAP_TYPE = {
        'int': 'MapType.INT',
        'String': 'MapType.STRING',
        'long': 'MapType.LONG',
        'Boolean': 'MapType.BOOLEAN',
        'Byte': 'MapType.BYTE',
        'Bean': 'MapType.BEAN'
    }

    Base_Read_Func = {'int': 'readInt()',
                      'String': 'readString()',
                      'long': 'readLong()',
                      'Boolean': 'readBoolean()',
                      'Byte': 'readByte()'
                      }

    Base_Write_Func = {'int': 'writeInt()',
                       'String': 'writeString()',
                       'long': 'writeLong()',
                       'Boolean': 'writeBoolean()',
                       'Byte': 'writeByte()'
                       }

    Base_Import = {
        'Message': 'com.common.connect.structure.Message',
        'long': 'com.common.connect.utils.long',
        'MapType': 'com.protocol.MapType'
    }

    pass
