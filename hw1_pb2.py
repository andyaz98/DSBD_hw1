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




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\thw1.proto\x12\x03hw1\"4\n\x13RegisterUserRequest\x12\r\n\x05\x65mail\x18\x01 \x01(\t\x12\x0e\n\x06ticker\x18\x02 \x01(\t\"2\n\x11UpdateUserRequest\x12\r\n\x05\x65mail\x18\x01 \x01(\t\x12\x0e\n\x06ticker\x18\x02 \x01(\t\"\"\n\x11\x44\x65leteUserRequest\x12\r\n\x05\x65mail\x18\x01 \x01(\t\"%\n\x12UserActionResponse\x12\x0f\n\x07outcome\x18\x01 \x01(\t\")\n\x18GetLastStockValueRequest\x12\r\n\x05\x65mail\x18\x01 \x01(\t\"R\n\x19GetLastStockValueResponse\x12\x0e\n\x06ticker\x18\x01 \x01(\t\x12\x12\n\nlast_value\x18\x02 \x01(\x02\x12\x11\n\ttimestamp\x18\x03 \x01(\t\"@\n\x1bGetStockPriceAverageRequest\x12\r\n\x05\x65mail\x18\x01 \x01(\t\x12\x12\n\nnum_values\x18\x02 \x01(\x05\"l\n\x1cGetStockPriceAverageResponse\x12\x0e\n\x06ticker\x18\x01 \x01(\t\x12\x15\n\raverage_price\x18\x02 \x01(\x02\x12\x12\n\nnum_values\x18\x03 \x01(\x05\x12\x11\n\ttimestamp\x18\x04 \x01(\t2\xda\x01\n\x11ManageUserService\x12\x43\n\x0cRegisterUser\x12\x18.hw1.RegisterUserRequest\x1a\x17.hw1.UserActionResponse\"\x00\x12?\n\nUpdateUser\x12\x16.hw1.UpdateUserRequest\x1a\x17.hw1.UserActionResponse\"\x00\x12?\n\nDeleteUser\x12\x16.hw1.DeleteUserRequest\x1a\x17.hw1.UserActionResponse\"\x00\x32\xbf\x01\n\x0cStockService\x12R\n\x11getLastStockValue\x12\x1d.hw1.GetLastStockValueRequest\x1a\x1e.hw1.GetLastStockValueResponse\x12[\n\x14getStockPriceAverage\x12 .hw1.GetStockPriceAverageRequest\x1a!.hw1.GetStockPriceAverageResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'hw1_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_REGISTERUSERREQUEST']._serialized_start=18
  _globals['_REGISTERUSERREQUEST']._serialized_end=70
  _globals['_UPDATEUSERREQUEST']._serialized_start=72
  _globals['_UPDATEUSERREQUEST']._serialized_end=122
  _globals['_DELETEUSERREQUEST']._serialized_start=124
  _globals['_DELETEUSERREQUEST']._serialized_end=158
  _globals['_USERACTIONRESPONSE']._serialized_start=160
  _globals['_USERACTIONRESPONSE']._serialized_end=197
  _globals['_GETLASTSTOCKVALUEREQUEST']._serialized_start=199
  _globals['_GETLASTSTOCKVALUEREQUEST']._serialized_end=240
  _globals['_GETLASTSTOCKVALUERESPONSE']._serialized_start=242
  _globals['_GETLASTSTOCKVALUERESPONSE']._serialized_end=324
  _globals['_GETSTOCKPRICEAVERAGEREQUEST']._serialized_start=326
  _globals['_GETSTOCKPRICEAVERAGEREQUEST']._serialized_end=390
  _globals['_GETSTOCKPRICEAVERAGERESPONSE']._serialized_start=392
  _globals['_GETSTOCKPRICEAVERAGERESPONSE']._serialized_end=500
  _globals['_MANAGEUSERSERVICE']._serialized_start=503
  _globals['_MANAGEUSERSERVICE']._serialized_end=721
  _globals['_STOCKSERVICE']._serialized_start=724
  _globals['_STOCKSERVICE']._serialized_end=915
# @@protoc_insertion_point(module_scope)
