"""Prompt templates for Vietnamese document drafting."""

from typing import Optional, Dict, Any


# System prompts
SYSTEM_PROMPT_GENERATE = """Bạn là chuyên gia soạn thảo văn bản phúc đáp, văn bản trả lời phản hồi chuyên nghiệp.

Nhiệm vụ: dựa trên văn bản gốc và văn bản phúc đáp mẫu, tạo văn bản phúc đáp theo format mẫu.

Yêu cầu:
- Output ở dạng Markdown đơn giản
- KHÔNG có câu dẫn hay kết luận
- CHỈ trả về nội dung văn bản phúc đáp

Cấu trúc output:
## TRÍCH YẾU
[Trích yếu văn bản]

## KÍNH GỬI
[Danh sách nơi nhận]

## NỘI DUNG
[Nội dung chính văn bản phúc đáp]

## KÝ TÊN
[Thông tin người ký]
"""

SYSTEM_PROMPT_REFINE = """Bạn là chuyên gia chỉnh sửa văn bản hành chính.

Nhiệm vụ: chỉnh sửa bản thảo văn bản theo yêu cầu của người dùng.

Yêu cầu:
- Giữ nguyên cấu trúc và format Markdown
- Chỉ thay đổi phần được yêu cầu
- Output TOÀN BỘ văn bản sau khi chỉnh sửa
"""


# Fewshot sample (simplified example)
# In production, this should be loaded from actual PDF extracts
FEWSHOT_SAMPLE_DEFAULT = """
### VĂN BẢN GỐC MẪU:
CÔNG TY LE DELTA
Số: 1217/VC-2026

CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc

Kính gửi: UBND Tỉnh Bắc Ninh

Công ty LE DELTA kính đề nghị UBND Tỉnh xem xét hỗ trợ về đất đai và chính sách ưu đãi đầu tư.

Trân trọng kính chào.

### VĂN BẢN PHÚC ĐÁP MẪU:
## TRÍCH YẾU
Về việc xem xét đề nghị của Công ty LE DELTA

## KÍNH GỬI
- Sở Tài chính
- Sở Kế hoạch và Đầu tư

## NỘI DUNG
UBND Tỉnh nhận được văn bản số 1217/VC-2026 của Công ty LE DELTA về việc đề nghị hỗ trợ.

UBND Tỉnh giao Sở Tài chính chủ trì, phối hợp Sở Kế hoạch và Đầu tư xem xét, báo cáo UBND Tỉnh trong thời hạn 10 ngày làm việc kể từ ngày nhận được văn bản này.

## KÝ TÊN
Nơi nhận:
- Như trên
- Lưu VP

CHỦ TỊCH
"""


def build_generate_prompt(
    file_content: str,
    metadata: Optional[Dict[str, Any]] = None,
    fewshot_sample: Optional[str] = None
) -> list[Dict[str, str]]:
    """
    Build messages for draft generation.

    Args:
        file_content: Extracted text from incoming document
        metadata: Optional metadata (trich_yeu, loai_van_ban, don_vi)
        fewshot_sample: Custom fewshot sample (defaults to FEWSHOT_SAMPLE_DEFAULT)

    Returns:
        List of message dicts for LLM chat completion
    """
    sample = fewshot_sample or FEWSHOT_SAMPLE_DEFAULT

    user_content = f"""### VĂN BẢN GỐC:
{file_content}

### VĂN BẢN PHÚC ĐÁP MẪU:
{sample}

Hãy soạn văn bản phúc đáp cho văn bản gốc trên, theo format của văn bản mẫu."""

    # Add metadata context if provided
    if metadata:
        meta_str = "\n".join(
            f"- {key}: {value}"
            for key, value in metadata.items()
            if value
        )
        if meta_str:
            user_content = f"""### METADATA:
{meta_str}

{user_content}"""

    return [
        {"role": "system", "content": SYSTEM_PROMPT_GENERATE},
        {"role": "user", "content": user_content}
    ]


def build_refine_prompt(
    current_draft: str,
    instruction: str
) -> list[Dict[str, str]]:
    """
    Build messages for draft refinement.

    Args:
        current_draft: Current draft content in markdown
        instruction: User's refinement instruction

    Returns:
        List of message dicts for LLM chat completion
    """
    user_content = f"""### BẢN THẢO HIỆN TẠI:
{current_draft}

### YÊU CẦU CHỈNH SỬA:
{instruction}

Hãy chỉnh sửa và trả về toàn bộ văn bản."""

    return [
        {"role": "system", "content": SYSTEM_PROMPT_REFINE},
        {"role": "user", "content": user_content}
    ]
