# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: hw1.proto
# Protobuf Python Version: 5.28.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    28,
    1,
    '',
    'hw1.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\thw1.proto\x12\x03hw1\")\n\x08Register\x12\r\n\x05\x65mail\x18\x01 \x01(\t\x12\x0e\n\x06ticker\x18\x02 \x01(\t\"\'\n\x06Update\x12\r\n\x05\x65mail\x18\x01 \x01(\t\x12\x0e\n\x06ticker\x18\x02 \x01(\t\"\x17\n\x06\x44\x65lete\x12\r\n\x05\x65mail\x18\x01 \x01(\t\"\x18\n\x05Reply\x12\x0f\n\x07outcome\x18\x01 \x01(\t\")\n\x18GetLastStockValueRequest\x12\r\n\x05\x65mail\x18\x01 \x01(\t\"R\n\x19GetLastStockValueResponse\x12\x0e\n\x06ticker\x18\x01 \x01(\t\x12\x12\n\nlast_value\x18\x02 \x01(\x02\x12\x11\n\ttimestamp\x18\x03 \x01(\t\"@\n\x1bGetStockPriceAverageRequest\x12\r\n\x05\x65mail\x18\x01 \x01(\t\x12\x12\n\nnum_values\x18\x03 \x01(\x05\"l\n\x1cGetStockPriceAverageResponse\x12\x0e\n\x06ticker\x18\x01 \x01(\t\x12\x15\n\raverage_price\x18\x02 \x01(\x02\x12\x12\n\nnum_values\x18\x03 \x01(\x05\x12\x11\n\ttimestamp\x18\x04 \x01(\t2\x94\x01\n\nManageUser\x12.\n\x0fRegisterMessage\x12\r.hw1.Register\x1a\n.hw1.Reply\"\x00\x12*\n\rUpdateMessage\x12\x0b.hw1.Update\x1a\n.hw1.Reply\"\x00\x12*\n\rDeleteMessage\x12\x0b.hw1.Delete\x1a\n.hw1.Reply\"\x00\x32\xbf\x01\n\x0cStockService\x12R\n\x11getLastStockValue\x12\x1d.hw1.GetLastStockValueRequest\x1a\x1e.hw1.GetLastStockValueResponse\x12[\n\x14getStockPriceAverage\x12 .hw1.GetStockPriceAverageRequest\x1a!.hw1.GetStockPriceAverageResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'hw1_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_REGISTER']._serialized_start=18
  _globals['_REGISTER']._serialized_end=59
  _globals['_UPDATE']._serialized_start=61
  _globals['_UPDATE']._serialized_end=100
  _globals['_DELETE']._serialized_start=102
  _globals['_DELETE']._serialized_end=125
  _globals['_REPLY']._serialized_start=127
  _globals['_REPLY']._serialized_end=151
  _globals['_GETLASTSTOCKVALUEREQUEST']._serialized_start=153
  _globals['_GETLASTSTOCKVALUEREQUEST']._serialized_end=194
  _globals['_GETLASTSTOCKVALUERESPONSE']._serialized_start=196
  _globals['_GETLASTSTOCKVALUERESPONSE']._serialized_end=278
  _globals['_GETSTOCKPRICEAVERAGEREQUEST']._serialized_start=280
  _globals['_GETSTOCKPRICEAVERAGEREQUEST']._serialized_end=344
  _globals['_GETSTOCKPRICEAVERAGERESPONSE']._serialized_start=346
  _globals['_GETSTOCKPRICEAVERAGERESPONSE']._serialized_end=454
  _globals['_MANAGEUSER']._serialized_start=457
  _globals['_MANAGEUSER']._serialized_end=605
  _globals['_STOCKSERVICE']._serialized_start=608
  _globals['_STOCKSERVICE']._serialized_end=799
# @@protoc_insertion_point(module_scope)