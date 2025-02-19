import json
from pydantic import BaseModel, Field
from typing import Dict, Optional, List

class InformationExtraction(BaseModel):
    """Pydantic model for Information Extraction metrics."""
    Average_IE_up: Optional[str] = Field(None, alias="Average IE ⬆️")
    NER: Optional[str] = None
    FINER_QRD: Optional[str] = Field(None, alias="FINER-QRD")
    FinRED: Optional[str] = None
    SC: Optional[str] = None
    CD: Optional[str] = None
    FNXL: Optional[str] = None
    FSRL: Optional[str] = None

class TextualAnalysis(BaseModel):
    """Pydantic model for Textual Analysis metrics."""
    Average_TA_up: Optional[str] = Field(None, alias="Average TA ⬆️")
    FPB: Optional[str] = None
    FiQA_SA: Optional[str] = Field(None, alias="FiQA-SA")
    Headlines: Optional[str] = None
    FOMC: Optional[str] = None
    FinArg_ACC: Optional[str] = Field(None, alias="FinArg-ACC")
    FinArg_ARC: Optional[str] = Field(None, alias="FinArg-ARC")
    MultiFin: Optional[str] = None
    MA: Optional[str] = None
    MLESG: Optional[str] = None

class QuestionAnswering(BaseModel):
    """Pydantic model for Question Answering metrics."""
    Average_QA_up: Optional[str] = Field(None, alias="Average QA ⬆️")
    FinQA: Optional[str] = None
    TATQA: Optional[str] = None
    ConvFinQA: Optional[str] = None

class TextGeneration(BaseModel):
    """Pydantic model for Text Generation metrics."""
    Average_TG_up: Optional[str] = Field(None, alias="Average TG ⬆️")
    EDTSUM: Optional[str] = None
    ECTSUM: Optional[str] = None

class RiskManagement(BaseModel):
    """Pydantic model for Risk Management metrics."""
    Average_RM_up: Optional[str] = Field(None, alias="Average RM ⬆️")
    German: Optional[str] = None
    Australian: Optional[str] = None
    LendingClub: Optional[str] = None
    ccf: Optional[str] = None
    ccfraud: Optional[str] = None
    polish: Optional[str] = None
    taiwan: Optional[str] = None
    portoseguro: Optional[str] = None
    travelinsurance: Optional[str] = None

class Forecasting(BaseModel):
    """Pydantic model for Forecasting metrics."""
    Average_FO_up: Optional[str] = Field(None, alias="Average FO ⬆️")
    BigData22: Optional[str] = None
    ACL18: Optional[str] = None
    CIKM18: Optional[str] = None

class DecisionMaking(BaseModel):
    """Pydantic model for Decision-Making metrics."""
    Average_DM_up: Optional[str] = Field(None, alias="Average DM ⬆️")
    FinTrade: Optional[str] = None

class ModelMetadata(BaseModel):
    """Pydantic model for a single model's metadata."""
    Model: str
    Average_up: Optional[str] = Field("", alias="Average ⬆️")
    Information_Extraction: InformationExtraction = Field(InformationExtraction(), alias="Information Extraction (IE)")
    Textual_Analysis: TextualAnalysis = Field(TextualAnalysis(), alias="Textual Analysis (TA)")
    Question_Answering: QuestionAnswering = Field(QuestionAnswering(), alias="Question Answering (QA)")
    Text_Generation: TextGeneration = Field(TextGeneration(), alias="Text Generation (TG)")
    Risk_Management: RiskManagement = Field(RiskManagement(), alias="Risk Management (RM)")
    Forecasting: Forecasting = Field(Forecasting(), alias="Forecasting (FO)")
    Decision_Making: DecisionMaking = Field(DecisionMaking(), alias="Decision-Making (DM)")

class MetadataContainer(BaseModel):
    """Pydantic model for the entire metadata container."""
    metadata: List[ModelMetadata]

def create_json_from_data(data_str: str) -> dict:
    """Converts the provided data string into the specified JSON format using Pydantic."""

    if not data_str.strip():
        return {"metadata": []}

    lines = data_str.strip().split('\n')
    header = lines[0].split(',')
    model_data = [line.split(',') for line in lines[1:]]

    metadata_list = []
    for row in model_data:
        model_dict = dict(zip(header, row))

        ie = InformationExtraction(
            Average_IE_up=model_dict.get("Average IE ⬆️"),
            NER=model_dict.get("NER"),
            FINER_QRD=model_dict.get("FINER-ORD"),
            FinRED=model_dict.get("FinRED"),
            SC=model_dict.get("SC"),
            CD=model_dict.get("CD"),
            FNXL=model_dict.get("FNXL"),
            FSRL=model_dict.get("FSRL")
        )

        ta = TextualAnalysis(
            Average_TA_up=model_dict.get("Average TA ⬆️"),
            FPB=model_dict.get("FPB"),
            FiQA_SA=model_dict.get("FiQA-SA"),
            Headlines=model_dict.get("Headlines"),
            FOMC=model_dict.get("FOMC"),
            FinArg_ACC=model_dict.get("FinArg-ACC"),
            FinArg_ARC=model_dict.get("FinArg-ARC"),
            MultiFin=model_dict.get("MultiFin"),
            MA=model_dict.get("MA"),
            MLESG=model_dict.get("MLESG")
        )

        qa = QuestionAnswering(
            Average_QA_up=model_dict.get("Average QA ⬆️"),
            FinQA=model_dict.get("FinQA"),
            TATQA=model_dict.get("TATQA"),
            ConvFinQA=model_dict.get("ConvFinQA")
        )

        tg = TextGeneration(
            Average_TG_up=model_dict.get("Average TG ⬆️"),
            EDTSUM=model_dict.get("EDTSUM"),
            ECTSUM=model_dict.get("ECTSUM")
        )

        rm = RiskManagement(
            Average_RM_up=model_dict.get("Average RM ⬆️"),
            German=model_dict.get("German"),
            Australian=model_dict.get("Australian"),
            LendingClub=model_dict.get("LendingClub"),
            ccf=model_dict.get("ccf"),
            ccfraud=model_dict.get("ccfraud"),
            polish=model_dict.get("polish"),
            taiwan=model_dict.get("taiwan"),
            portoseguro=model_dict.get("portoseguro"),
            travelinsurance=model_dict.get("travelinsurance")
        )

        fo = Forecasting(
            Average_FO_up=model_dict.get("Average FO ⬆️"),
            BigData22=model_dict.get("BigData22"),
            ACL18=model_dict.get("ACL18"),
            CIKM18=model_dict.get("CIKM18")
        )

        dm = DecisionMaking(
            Average_DM_up=model_dict.get("Average DM ⬆️"),
            FinTrade=model_dict.get("FinTrade")
        )

        model_metadata = ModelMetadata(
            Model=model_dict.get("Model"),
            Average_up=model_dict.get("Average ⬆️"),
            Information_Extraction=ie,
            Textual_Analysis=ta,
            Question_Answering=qa,
            Text_Generation=tg,
            Risk_Management=rm,
            Forecasting=fo,
            Decision_Making=dm
        )
        metadata_list.append(model_metadata)

    return MetadataContainer(metadata=metadata_list).dict()


# Example Usage with empty data string
empty_data_str = """
T
Model
Average ⬆️
Average IE ⬆️
Average TA ⬆️
Average QA ⬆️
Average TG ⬆️
Average RM ⬆️
Average FO ⬆️
Average DM ⬆️
Type
Architecture
Precision
Hub License
#Params (B)
Hub ❤️
Available on the hub
Model sha
FPB
FiQA-SA
TSA
Headlines
FOMC
FinArg-ACC
FinArg-ARC
MultiFin
MA
MLESG
NER
FINER-ORD
FinRED
SC
CD
FinQA
TATQA
ConvFinQA
FNXL
FSRL
EDTSUM
ECTSUM
BigData22
ACL18
CIKM18
German
Australian
LendingClub
ccf
ccfraud
polish
taiwan
portoseguro
travelinsurance
FinTrade

⭕
TheFinAI/finma-7b-full

21.5
12.6
48.7
8
6.5
49.7
50.7
0
instruction-tuned
?
float16
?
0
0
0
main
88
79
80
97
49
27
8
14
45
0
69
0
0
19
0
4
0
20
0
0
13
0
51
51
50
50
50
50
50
47
49.5
50
50.5
50
missing
🟢
internlm/internlm-7b

20.4
12.6
47.3
0
6.5
50.2
54.7
0
pretrained
InternLMForCausalLM
float16
?
0
0
1
main
69
81
29
60
36
39
33
34
78
14
0
0
0
88
0
0
0
0
0
0
13
0
56
51
57
35
56.5
57.5
50
43.5
53.5
49.5
50
56
missing
🟢
THUDM/chatglm3-6b

20.3
15.4
49.5
2.3
6.5
47.8
46.3
0
pretrained
ChatGLMModel
float16
?
0
0
1
main
74
56
35
66
47
25
50
47
79
16
25
2
0
81
0
0
7
0
0
0
13
0
47
50
42
35
49
48.5
50
42.5
50
50.5
53
51.5
missing
🔶
meta-llama/Llama-2-7b-chat-hf

19.9
15
45.9
1
8.5
48.9
53.3
0
fine-tuned
?
float16
?
0
0
0
main
39
76
71
72
35
46
27
20
70
3
18
2
0
85
0
0
3
0
0
0
17
0
54
51
55
51.5
50
50
50
42
50
49.5
47.5
50
missing
🟢
meta-llama/Llama-3.2-3B-Instruct

19.9
12.8
50
0.1
0
50.3
49.6
0
pretrained
?
float16
?
0
0
0
main
63.9
74.4
16.4
60.3
43.5
42.8
48.9
missing
missing
missing
1.8
0.2
0.2
87.2
0
0
0.4
0
0
0
missing
missing
46.7
49.8
52.4
51.8
50
50
50
50
51.7
50
49.2
50
missing
🟢
mistralai/Mixtral-8x7B-v0.1

19.4
16
37.6
10.7
6
51.4
45.7
0
pretrained
?
float16
?
0
0
0
main
29
16
50
60
37
39
57
37
34
17
24
5
0
83
0
0
1
31
0
0
12
0
46
49
42
50
50
54
50
58
50
50
50.5
50
missing
🟢
bigcode/starcoder2-7b

17.6
13.1
35
0
0
49.9
50.5
0
pretrained
?
float16
?
0
0
0
main
46.1
31.7
36.9
60
34.7
13.5
46.2
31.8
35.2
13.7
6.4
1.7
0.5
82.9
0.2
0
0.1
0
0
0
missing
missing
53.1
50.1
48.3
50
50
50
49.3
50
50
50
50
50
missing
🔶
tiiuae/falcon-7b-instruct

17.5
1.2
40.7
2.3
0
49.6
49.8
0
fine-tuned
FalconForCausalLM
float16
?
0
0
1
main
64.3
74.5
41
44.7
28.9
37.3
57
19.1
34.9
5.2
0
0
0
8.2
0
0.2
6.6
0
0
0
missing
missing
55.2
50.6
43.7
50
50
50
49.8
42.4
50
50
50
54.5
missing
🟢
codellama/CodeLlama-7b-hf

16.7
13.1
35.5
0
5
50
51.3
0
pretrained
LlamaForCausalLM
float16
?
0
0
1
main
34
66
43
60
14
28
25
21
54
10
7
0
0
85
0
0
0
0
0
0
10
0
52
51
51
50
50
50
50
50
52
48.5
49.5
50
missing
🔶
Go4miii/DISC-FinLLM

15.3
1.7
31.7
0
11
49.8
46
0
fine-tuned
BaichuanForCausalLM
float16
?
0
0
1
main
29
32
32
60
19
29
29
29
29
29
12
0
0
0
0
0
0
0
0
0
22
0
44
50
44
50
50
50
48
51
50
50
49
50
missing
🟢
baichuan-inc/Baichuan-7B

14.2
8.1
29.5
0
1
49.8
50.3
0
pretrained
BaiChuanForCausalLM
float16
?
0
0
1
main
36
17
107
60
16
34
17
6
2
0
0
0
0
57
0
0
0
0
0
0
2
0
53
50
48
50
50
51
50
48
49.5
50
50
50
missing
⭕
TongjiFinLab/CFGPT1-sft-7B-Full

12.6
2.1
30
0.3
0.5
49.5
44.7
0
instruction-tuned
InternLMForCausalLM
float16
?
0
0
1
main
35
42
105
61
16
5
5
5
25
1
0
0
0
15
0
0
0
1
0
0
1
0
45
48
41
50
45
50.5
50
50.5
49
50
50
50.5
missing
⭕
FinGPT/fingpt-mt_llama2-7b_lora

8.5
0
11
0
0
50.2
47.7
0
instruction-tuned
?
float16
?
0
0
0
main
0
0
50
60
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
45
49
49
50
50
50
50
50
51
50.5
50
50
missing


"""
result_json = create_json_from_data(empty_data_str)

with open("finbench_leaderboard_complete.json", "w") as jsonFile:
    json.dump(result_json, jsonFile)
