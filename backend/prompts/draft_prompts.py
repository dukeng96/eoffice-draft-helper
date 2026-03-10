"""Prompt templates for Vietnamese document drafting."""

from typing import Optional, Dict, Any


SYSTEM_PROMPT_GENERATE = """Bạn là chuyên gia soạn thảo văn bản hành chính của Văn phòng UBND Thành phố Hà Nội.

Nhiệm vụ: Dựa trên văn bản đến (VB đến) và các mẫu phiếu trình bên dưới, soạn phiếu trình xử lý phù hợp.

Yêu cầu:
- Output ở dạng Markdown
- KHÔNG có câu dẫn hay kết luận ngoài nội dung văn bản
- CHỈ trả về nội dung phiếu trình
- Bám sát format và giọng văn của các mẫu"""


SYSTEM_PROMPT_REFINE = """Bạn là chuyên gia chỉnh sửa văn bản hành chính.

Nhiệm vụ: chỉnh sửa bản thảo văn bản theo yêu cầu của người dùng.

Yêu cầu:
- Giữ nguyên cấu trúc và format Markdown
- Chỉ thay đổi phần được yêu cầu
- Output TOÀN BỘ văn bản sau khi chỉnh sửa
"""


# ============================================================
# FEWSHOT SAMPLES — chỉnh sửa tại đây để thêm/bớt/thay mẫu
# ============================================================
FEWSHOT_SAMPLES = """
=== MẪU 1 ===

VĂN BẢN ĐẾN:
CÔNG TY CỔ PHẦN LE DELTAKính gửi: * Thành uỷ Thành phố Hà NộiUỷ ban nhân dân Thành phố Hà NộiCông ty cổ phần Le Delta xin gửi lời chào trân trọng và lời chúc sức khỏe đến lãnh đạo Quý cơ quan!Công ty cổ phần Le Delta là doanh nghiệp hoạt động theo giấy chứng nhận đăng ký kinh doanh số 010181321, do Sở Kế hoạch và Đầu tư thành phố Hà Nội cấp lần đầu ngày 31/10/2005. Vốn điều lệ của Công ty hiện nay là 2.500 tỷ đồng. Địa chỉ trụ sở tại số A6 lô A, Khu 5.2ha, dự án nhà ở cho cán bộ cao cấp và cán bộ của Ban Đảng Trung ương, phường Yên Hoà, quận Cầu Giấy, thành phố Hà Nội.Công ty cổ phần Le Delta là doanh nghiệp trong các lĩnh vực: xử lý chất thải kết hợp thu hồi năng lượng, năng lượng sạch; thiết bị y tế, giáo dục; đầu tư xây dựng kết cấu hạ tầng Khu công nghiệp, khu đô thị, quản lý chiếu sáng công cộng, cây xanh, hệ thống thoát nước, cùng các dịch vụ hạ tầng kỹ thuật và môi trường đô thị quy mô lớn trên nhiều tỉnh thành trên cả nước như: tp.Hà Nội, tp. HCM, Phú Thọ, Bắc Ninh, Thanh Hoá, Hưng Yên, ....Với đội ngũ cán bộ kỹ sư, chuyên gia giàu kinh nghiệm, hệ thống thiết bị hiện đại, cùng năng lực quản lý dự án chuyên nghiệp, Công ty cổ phần Le Delta luôn tiên phong trong việc ứng dụng các công nghệ xử lý chất thải tiên tiến, thúc đẩy phát triển năng lượng tái tạo và kinh tế tuần hoàn, hướng tới mục tiêu xây dựng môi trường xanh – sạch – hiện đại – bền vững cho các đô thị Việt Nam. Đối với lĩnh vực xử lý chất thải Công ty chúng tôi đã có kinh nghiệm triển khai dự án và đã áp dụng công nghệ lò đốt ghi cơ học tiên tiến kiểu Waterleau của Bỉ là một dây chuyền công nghệ, thiết bị đồng bộ, hiện đại, thân thiện với môi trường; nhiệt năng được thu hồi để phát điện; đáp ứng tiêu chuẩn, quy chuẩn môi trường của Việt Nam và Châu Âu.Một số các dự án xử lý chất thải rắn thu hồi năng lượng tại Việt Nam đã triển khai, vận hành thành công như:Dự án Nhà máy điện rác Sóc Sơn, Hà Nội có công suất tiếp nhận và xử lý 5.000 tấn chất thải rắn/ngày đêm công suất phát điện 90MW;Dự án Nhà máy xử lý chất thải rắn, phát điện tại xã Trạm Thản, tỉnh Phú Thọ có tổng quy mô 1.000 tấn/ngày và công suất phát điện là 18MW;Dự án Nhà máy xử lý chất thải rắn, phát điện tại phường Bỉm Sơn, tỉnh Thanh Hóa có tổng quy mô 1.000 tấn/ngày và công suất phát điện là 18MW;Dự án Nhà máy điện rác Phù Cừ tại xã Đoàn Đào, tỉnh Hưng Yên có tổng quy mô 1.600 tấn/ngày và công suất phát điện 40MW.Qua nghiên cứu đánh giá thực trạng các vấn đề phát sinh chất thải, xử lý chất thải trên địa bàn thành phố Hà Nội Liên danh nhà đầu tư chúng tôi nhận thấy: Hà Nội là đô thị đặc biệt, trung tâm chính trị - hành chính quốc gia với quy mô dân số trên 8 triệu người... Từ những thực trạng nêu trên, Công ty cổ phần Le Delta xin đề xuất đầu tư dự án Nhà máy xử lý bùn thải và chất thải rắn bằng công nghệ đốt phát điện Hà Nội với những nội dung như sau:Tên dự án: Nhà máy xử lý bùn thải và chất thải rắn bằng công nghệ đốt phát điện tại thành phố Hà Nội.Địa điểm: Xã Chương Dương, Thành phố Hà Nội.Diện tích sử dụng đất: 94.697 m2. Công suất tiếp nhận và xử lý: Bùn thải: 3.000 tấn/ngày; CTRSH: 1.500 tấn/ngày; CTR công nghiệp thông thường: 300-500 tấn/ngày. Công nghệ: Lò đốt ghi cơ học tiên tiến kiểu Waterleau – Bỉ. Số lượng lò đốt: 03 lò, mỗi lò công suất 800 tấn/ngày. Công suất phát điện: 60 MW. Vốn đầu tư: 7.420.000.000.000 đồng (280 triệu USD). Nhà đầu tư kính đề nghị Thành uỷ, UBND Thành phố xem xét, chấp thuận chủ trương đầu tư.Trân trọng!

VĂN BẢN ĐI:
# PHIẾU TRÌNH XỬ LÝ CÔNG VIỆC

**Kính gửi:** Phó Chủ tịch UBND Thành phố Nguyễn Mạnh Quyền.

|  |  |
| --- | --- |
| **Vấn đề trình:** | Kiểm tra, xem xét nội dung đề nghị của Công ty cổ phần Le Delta tại Văn bản số 09/LDT-PTDA ngày 29/01/2026 |
| **Cơ quan trình:** | Công ty cổ phần Le Delta |
| **Văn bản kèm theo:** | Văn bản số 09/LDT-PTDA ngày 29/01/2026 của Công ty cổ phần Le Delta |

### Ý kiến phê duyệt, chỉ đạo của Phó Chủ tịch UBND Thành phố

---

### I. Tóm tắt nội dung:

Tại Văn bản số 09/LDT-PTDA ngày 29/01/2026 của Công ty cổ phần Le Delta báo cáo, đề nghị UBND Thành phố cho phép nghiên cứu đầu tư dự án xử lý bùn thải và chất thải rắn với nội dung chính như sau:

1. **Tên dự án:** Nhà máy xử lý bùn thải và chất thải rắn bằng công nghệ đốt phát điện tại thành phố Hà Nội.
2. **Địa điểm:** Xã Chương Dương, Thành phố Hà Nội.
3. **Mục tiêu:** Đầu tư xây dựng nhà máy xử lý bùn thải và chất thải rắn bằng công nghệ đốt hiện đại; nhiệt năng từ quá trình đốt được thu hồi và sinh hơi phát điện.
4. **Diện tích sử dụng đất:** 94.697 m²
5. **Quy mô đầu tư:**
   - Bùn thải: 3.000 tấn/ngày; CTRSH: 1.500 tấn/ngày; CTR công nghiệp thông thường: 300–500 tấn/ngày
   - Công nghệ: Lò đốt ghi cơ học tiên tiến, kiểu Waterleau – Bỉ
   - Số lượng lò đốt: 03 lò, mỗi lò công suất 800 tấn/ngày
   - Công suất phát điện: 60 MW (2 tổ máy, mỗi tổ 30 MW)
6. **Vốn đầu tư:** 7.420.000.000.000 đồng (280 triệu USD)
7. **Nhà đầu tư đề nghị:** Chấp thuận chủ trương đầu tư Dự án

### II. Báo cáo và đề xuất của Văn phòng:

Trên cơ sở nội dung báo cáo, đề nghị của Công ty cổ phần Le Delta, căn cứ chức năng, nhiệm vụ của Sở Tài chính, Văn phòng kính đề nghị Phó Chủ tịch có ý kiến chỉ đạo với nội dung như sau: *"Giao Sở Tài chính chủ trì, phối hợp với các đơn vị liên quan kiểm tra, xem xét nội dung đề nghị của Công ty cổ phần Le Delta tại Văn bản số 09/LDT-PTDA ngày 29/01/2026; tham mưu, đề xuất, báo cáo UBND Thành phố theo quy định **trước ngày 12/03/2026**."*

Kính báo cáo Phó Chủ tịch xem xét, quyết định./.


=== MẪU 2 ===

VĂN BẢN ĐẾN:
TỜ TRÌNH Về việc ban hành Kế hoạch tổ chức phong trào thi đua "Doanh nghiệp Thủ đô đổi mới sáng tạo, hội nhập và phát triển" giai đoạn 2026 - 2030 Kính gửi: Ủy ban nhân dân thành phố Hà Nội. Thực hiện Kế hoạch số 371/KH-UBND ngày 26/12/2025 của UBND thành phố Hà Nội về Kế hoạch công tác thi đua, khen thưởng năm 2026. Theo đó, giao Sở Tài chính chủ trì, phối hợp với Sở Nội vụ (Ban Thi đua – Khen thưởng), các ngành, đơn vị liên quan tham mưu trình UBND Thành phố Kế hoạch trước ngày 28/02/2026; Căn cứ các giải pháp, chỉ tiêu được nêu tại Nghị quyết số 68-NQ/TW ngày 04/5/2025 của Bộ Chính trị về phát triển kinh tế tư nhân; Nghị quyết số 79 NQ/TW ngày 06/01/2026 của Bộ Chính trị về phát triển kinh tế nhà nước; và các góp ý của Sở Nội vụ (Ban Thi đua – Khen thưởng Thành phố) tại văn bản số 72/BTĐ-NV2 ngày 03/02/2026; Sở Tài chính đã phối hợp với Sở Nội vụ (Ban Thi đua – Khen thưởng Thành phố) dự thảo Kế hoạch tổ chức phong trào thi đua "Doanh nghiệp Thủ đô đổi mới sáng tạo, hội nhập và phát triển" giai đoạn 2026 – 2030 (theo dự thảo đính kèm). Sở Tài chính kính trình UBND thành phố Hà Nội xem xét, phê duyệt. Trân trọng./

VĂN BẢN ĐI:
# PHIẾU TRÌNH XỬ LÝ VĂN BẢN

*Hà Nội, ngày 27 tháng 02 năm 2026*

**Kính gửi:** Đ/c Dương Đức Tuấn, Phó Chủ tịch Thường trực UBND Thành phố

|  |  |
| --- | --- |
| **Vấn đề trình:** | Sở Tài chính có Tờ trình số 1941/TTr-STC ngày 09/02/2026 về việc trình ban hành Kế hoạch tổ chức phong trào thi đua "Doanh nghiệp Thủ đô đổi mới sáng tạo, hội nhập và phát triển" giai đoạn 2026 - 2030. |

### I. Ý kiến chỉ đạo của Phó Chủ tịch Thường trực UBND Thành phố

---

### III. Văn phòng UBND Thành phố báo cáo

#### 1. Báo cáo và đề nghị của Sở Tài chính

Thực hiện Kế hoạch số 371/KH-UBND ngày 26/12/2025 của UBND thành phố Hà Nội về Kế hoạch công tác thi đua, khen thưởng năm 2026. Theo đó, giao Sở Tài chính chủ trì, phối hợp với Sở Nội vụ (Ban Thi đua – Khen thưởng), các ngành, đơn vị liên quan tham mưu trình UBND Thành phố ban hành Kế hoạch tổ chức phong trào thi đua "Doanh nghiệp Thủ đô đổi mới sáng tạo, hội nhập và phát triển" giai đoạn 2026 - 2030 trước ngày 28/02/2026.

Sở Tài chính đã phối hợp với Sở Nội vụ (Ban Thi đua – Khen thưởng Thành phố) dự thảo Kế hoạch tổ chức phong trào thi đua "Doanh nghiệp Thủ đô đổi mới sáng tạo, hội nhập và phát triển" giai đoạn 2026 - 2030.

#### 2. Ý kiến đề xuất của Văn phòng:

Sau khi rà soát, Văn phòng UBND Thành phố báo cáo:
Ngày 05/02/2026, Bộ Nội vụ có văn bản số 1151/BNV-BTĐKTTW xin ý kiến dự thảo Quyết định của Thủ tướng Chính phủ ban hành Kế hoạch triển khai Phong trào thi đua "Phát triển doanh nghiệp tư nhân, nâng cao hiệu quả doanh nghiệp nhà nước", do đó nội dung trình của Sở Tài chính cần cập nhật, bổ sung nội dung sau khi Thủ tướng Chính phủ ban hành Kế hoạch triển khai Phong trào thi đua nêu trên.

Văn phòng tham mưu văn bản chỉ đạo của Phó Chủ tịch Thường trực UBND Thành phố:
Giao Sở Tài chính chủ trì, phối hợp với cơ quan, đơn vị liên quan cập nhật, bổ sung, tổng hợp nội dung phong trào thi đua "Phát triển doanh nghiệp tư nhân, nâng cao hiệu quả doanh nghiệp nhà nước" sau khi được Thủ tướng Chính phủ phê duyệt, ký ban hành vào nội dung Kế hoạch của UBND Thành phố về tổ chức phong trào thi đua "Doanh nghiệp Thủ đô đổi mới sáng tạo, hội nhập và phát triển" giai đoạn 2026 – 2030.

Văn phòng kính báo cáo Phó Chủ tịch Thường trực UBND Thành phố xem xét, phê duyệt.


=== MẪU 3 ===

VĂN BẢN ĐẾN:
THÔNG TƯ Quy định quản lý, vận hành Hệ thống đăng ký quốc gia về hạn ngạch phát thải khí nhà kính và tín chỉ các-bon Căn cứ Luật Bảo vệ môi trường số 72/2020/QH14 được sửa đổi, bổ sung một số điều bởi các Luật số 11/2022/QH15, 16/2023/QH15, 18/2023/QH15, 47/2024/QH15, 54/2024/QH15 và 146/2025/QH15; Căn cứ Nghị định số 06/2022/NĐ-CP ngày 07/01/2022 của Chính phủ quy định giảm nhẹ phát thải khí nhà kính và bảo vệ tầng ô-dôn được sửa đổi, bổ sung bởi Nghị định số 119/2025/NĐ-CP ngày 09/6/2025; Căn cứ Nghị định số 29/2026/NĐ-CP ngày 19/01/2026 của Chính phủ về sàn giao dịch các-bon trong nước; Căn cứ Nghị định số 35/2025/NĐ-CP ngày 25/02/2025 quy định chức năng, nhiệm vụ, quyền hạn và cơ cấu tổ chức của Bộ Nông nghiệp và Môi trường; Theo đề nghị của Cục trưởng Cục Biến đổi khí hậu; Bộ trưởng Bộ Nông nghiệp và Môi trường ban hành Thông tư quy định quản lý, vận hành Hệ thống đăng ký quốc gia về hạn ngạch phát thải khí nhà kính và tín chỉ các-bon. Chương I - QUY ĐỊNH CHUNG. Điều 1. Phạm vi điều chỉnh: Thông tư này quy định về việc quản lý, vận hành Hệ thống đăng ký quốc gia về hạn ngạch phát thải khí nhà kính và tín chỉ các-bon (sau đây gọi là Hệ thống đăng ký quốc gia). Điều 2. Đối tượng áp dụng: Thông tư này áp dụng đối với các cơ quan, tổ chức: (1) Đơn vị trực thuộc Bộ Nông nghiệp và Môi trường; (2) Tổng công ty lưu ký và bù trừ chứng khoán Việt Nam (VSDC); (3) Sở Giao dịch chứng khoán Việt Nam (VNX); (4) Sở Giao dịch chứng khoán Hà Nội (HNX); (5) Cơ quan, tổ chức có cơ sở được phân bổ hạn ngạch phát thải khí nhà kính; (6) Cơ quan, tổ chức trên lãnh thổ Việt Nam có chương trình, dự án đăng ký theo các cơ chế trao đổi, bù trừ tín chỉ các-bon; (7) Cơ quan, tổ chức khác có liên quan.

VĂN BẢN ĐI:
# PHIẾU TRÌNH GIẢI QUYẾT CÔNG VIỆC

**Kính gửi:** Phó Chủ tịch UBND Thành phố Nguyễn Mạnh Quyền

**Vấn đề trình:** UBND Thành phố nhận được Thông tư số 11/2026/TT-BNNMT ngày 13/02/2026 của Bộ trưởng Bộ Nông nghiệp và Môi trường quy định quản lý, vận hành Hệ thống đăng ký quốc gia về hạn ngạch phát thải khí nhà kính và tín chỉ các-bon

---

### Ý kiến chỉ đạo của Phó Chủ tịch UBND TP

---

### Báo cáo, đề xuất của Văn phòng.

Văn phòng UBND Thành phố báo cáo Phó Chủ tịch UBND Thành phố biết và cho phép Văn phòng thông báo đến Sở Nông nghiệp và Môi trường, UBND các phường, xã biết, truy cập, nghiên cứu, thực hiện.

**(có dự thảo kèm theo).**

Văn phòng kính báo cáo Phó Chủ tịch UBND Thành phố xem xét, chỉ đạo./.
"""

# Alias để tương thích ngược với code cũ
FEWSHOT_SAMPLE_DEFAULT = FEWSHOT_SAMPLES


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
        fewshot_sample: Custom fewshot sample (defaults to FEWSHOT_SAMPLES)

    Returns:
        List of message dicts for LLM chat completion
    """
    sample = fewshot_sample or FEWSHOT_SAMPLES

    user_content = f"""### CÁC MẪU THAM KHẢO:
{sample}

### VĂN BẢN ĐẾN CẦN XỬ LÝ:
{file_content}

Hãy soạn phiếu trình xử lý cho văn bản đến trên, theo format và giọng văn của các mẫu tham khảo."""

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
