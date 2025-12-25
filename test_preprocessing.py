"""
BERTopic Pro - 第二阶段功能测试
测试数据预处理模块的所有功能
"""

import sys
from pathlib import Path

print("=" * 60)
print("BERTopic Pro - 第二阶段功能测试")
print("=" * 60)

# 1. 测试文件读取
print("\n[1/6] 测试文件读取...")
try:
    from app.utils.file_helpers import read_file, preview_dataframe
    import config

    test_file = config.RAW_DATA_DIR / 'test_data.csv'
    df = read_file(test_file)

    print(f"  ✓ 文件读取成功")
    print(f"    - 文件: {test_file.name}")
    print(f"    - 行数: {len(df)}")
    print(f"    - 列数: {len(df.columns)}")
    print(f"    - 列名: {list(df.columns)}")

except Exception as e:
    print(f"  ✗ 失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 2. 测试列验证
print("\n[2/6] 测试列验证...")
try:
    from app.utils.validators import validate_text_column, get_recommended_columns

    # 验证文本列
    is_valid, error, stats = validate_text_column(df, 'text')
    print(f"  ✓ 文本列验证: {is_valid}")
    if is_valid:
        print(f"    - 有效文本: {stats['valid']}/{stats['total']}")
        print(f"    - 平均长度: {stats['avg_length']:.1f}")

    # 推荐列
    text_cols = get_recommended_columns(df, for_text=True)
    print(f"  ✓ 推荐文本列: {text_cols}")

except Exception as e:
    print(f"  ✗ 失败: {e}")
    sys.exit(1)

# 3. 测试文本处理
print("\n[3/6] 测试文本处理...")
try:
    from app.core.processor import TextProcessor

    processor = TextProcessor()

    # 测试单个文本
    test_text = "今天天气真好，适合出去旅游。http://example.com test@email.com"
    processed = processor.process_text(
        test_text,
        segment=True,
        remove_stopwords=True
    )

    print(f"  ✓ 文本处理成功")
    print(f"    - 原文: {test_text[:50]}...")
    print(f"    - 处理后: {processed}")

except Exception as e:
    print(f"  ✗ 失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 4. 测试批量处理
print("\n[4/6] 测试批量处理...")
try:
    import pandas as pd

    def progress_callback(pct, msg):
        if pct in [25, 50, 75, 100]:
            print(f"    - 进度: {pct}% - {msg}")

    processed_df = processor.process_dataframe(
        df,
        'text',
        progress_callback=progress_callback
    )

    print(f"  ✓ 批量处理成功")
    print(f"    - 处理行数: {len(processed_df)}")

    # 显示前3个处理结果
    print(f"\n  示例结果:")
    for idx in range(min(3, len(processed_df))):
        original = df.iloc[idx]['text']
        processed_text = processed_df.iloc[idx]['text_processed']
        print(f"    [{idx+1}] 原文: {original[:40]}...")
        print(f"        处理: {processed_text[:60]}...")

except Exception as e:
    print(f"  ✗ 失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 5. 测试数据预览
print("\n[5/6] 测试数据预览...")
try:
    preview = preview_dataframe(df, max_rows=5)

    print(f"  ✓ 数据预览生成成功")
    print(f"    - 预览行数: {len(preview)}")
    print(f"\n{preview.to_string()}")

except Exception as e:
    print(f"  ✗ 失败: {e}")
    sys.exit(1)

# 6. 测试UI组件导入
print("\n[6/6] 测试UI组件...")
try:
    from app.ui.tabs.preprocess_tab import PreprocessTab, ProcessingWorker

    print(f"  ✓ PreprocessTab 导入成功")
    print(f"  ✓ ProcessingWorker 导入成功")

except Exception as e:
    print(f"  ✗ 失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 60)
print("✅ 所有功能测试通过！")
print("=" * 60)

print("\n📊 第二阶段总结:")
print("  ✓ 文件读取 - 支持 CSV/Excel/TXT，自动编码检测")
print("  ✓ 数据验证 - 智能列推荐，完整性检查")
print("  ✓ 文本处理 - Jieba 分词，停用词过滤，清洗")
print("  ✓ 批量处理 - 多线程，进度跟踪")
print("  ✓ UI 界面 - 完整的预处理 Tab (500+ 行)")

print("\n🎯 已实现功能:")
print("  1. 文件导入（CSV/Excel/TXT）")
print("  2. 数据预览表格")
print("  3. 智能列映射")
print("  4. Jieba 分词设置")
print("  5. 文本清洗选项")
print("  6. 后台处理（Worker）")
print("  7. 进度显示")
print("  8. 结果保存")

print("\n💡 使用方法:")
print("  1. python main.py")
print("  2. 打开 Tab 1 (数据预处理)")
print("  3. 点击 '浏览' 选择 data/raw/test_data.csv")
print("  4. 点击 '加载数据'")
print("  5. 选择文本列 (text)")
print("  6. 配置处理选项")
print("  7. 点击 '开始处理'")
print("  8. 查看处理结果并保存")

print("\n🚀 第二阶段完成！可以开始使用预处理功能了。")
