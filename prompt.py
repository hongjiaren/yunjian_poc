

HARDWARE_ANALYSIS_PROMPT = """
请分析这张图片，并提取其中的所有硬件设备及其相关信息（包括被测设备、测试环境、编码、数量和备注说明）。请以如下 JSON 格式返回结果：

{
  "test_configuration": [
    {
      "device": "被测设备名称",
      "environment": "测试环境1",
      "code": "编码1",
      "quantity": "数量1",
      "note": "备注说明"
    },{
      "device": "被测设备名称",
      "environment": "测试环境2",
      "code": "编码2",
      "quantity": "数量2",
      "note": "备注说明"2
    }
    ...
  ]
}

注意：
- 被测设备只有一个，其名称为 "xxx"。在图片中一般数字和字母的组合。
- 测试环境包括以下几种的一种：PC, 网线, 串口线, 对接网线工装, PTS测试仪, SFP+光模块, 光纤, S5590-9P-SI, 环境U盘, ONIE启动U盘, PDU, 环境电源, 环境风扇。
- 如果某个字段无具体值，则留空。
- 示例数据结构如下：
  - device: "48T6X"
  - environment: "PC"
  - code: ""
  - quantity: "1"
  - note: "PIII700以上,带双网口,双串口卡"
- 直接输出json
"""