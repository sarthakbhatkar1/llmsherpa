import json
import re
from pydantic import BaseModel, Field
from typing import Optional, List
class InformationExtraction(BaseModel):
    """Pydantic model for Information Extraction metrics."""
    average_ie_up: Optional[str] = Field("", alias="average_ie_up")
    ner: Optional[str] = Field("", alias="ner")
    finer_qrd: Optional[str] = Field("", alias="finer_qrd")
    finred: Optional[str] = Field("", alias="finred")
    sc: Optional[str] = Field("", alias="sc")
    cd: Optional[str] = Field("", alias="cd")
    fnxl: Optional[str] = Field("", alias="fnxl")
    fsrl: Optional[str] = Field("", alias="fsrl")

class TextualAnalysis(BaseModel):
    """Pydantic model for Textual Analysis metrics."""
    average_ta_up: Optional[str] = Field("", alias="average_ta_up")
    fpb: Optional[str] = Field("", alias="fpb")
    fiqa_sa: Optional[str] = Field("", alias="fiqa_sa")
    headlines: Optional[str] = Field("", alias="headlines")
    fomc: Optional[str] = Field("", alias="fomc")
    finarg_acc: Optional[str] = Field("", alias="finarg_acc")
    finarg_arc: Optional[str] = Field("", alias="finarg_arc")
    multifin: Optional[str] = Field("", alias="multifin")
    ma: Optional[str] = Field("", alias="ma")
    mlesg: Optional[str] = Field("", alias="mlesg")

class QuestionAnswering(BaseModel):
    """Pydantic model for Question Answering metrics."""
    average_qa_up: Optional[str] = Field("", alias="average_qa_up")
    finqa: Optional[str] = Field("", alias="finqa")
    tatqa: Optional[str] = Field("", alias="tatqa")
    convfinqa: Optional[str] = Field("", alias="convfinqa")

class TextGeneration(BaseModel):
    """Pydantic model for Text Generation metrics."""
    average_tg_up: Optional[str] = Field("", alias="average_tg_up")
    edtsum: Optional[str] = Field("", alias="edtsum")
    ectsum: Optional[str] = Field("", alias="ectsum")

class RiskManagement(BaseModel):
    """Pydantic model for Risk Management metrics."""
    average_rm_up: Optional[str] = Field("", alias="average_rm_up")
    german: Optional[str] = Field("", alias="german")
    australian: Optional[str] = Field("", alias="australian")
    lendingclub: Optional[str] = Field("", alias="lendingclub")
    ccf: Optional[str] = Field("", alias="ccf")
    ccfraud: Optional[str] = Field("", alias="ccfraud")
    polish: Optional[str] = Field("", alias="polish")
    taiwan: Optional[str] = Field("", alias="taiwan")
    portoseguro: Optional[str] = Field("", alias="portoseguro")
    travelinsurance: Optional[str] = Field("", alias="travelinsurance")

class Forecasting(BaseModel):
    """Pydantic model for Forecasting metrics."""
    average_fo_up: Optional[str] = Field("", alias="average_fo_up")
    bigdata22: Optional[str] = Field("", alias="bigdata22")
    acl18: Optional[str] = Field("", alias="acl18")
    cikm18: Optional[str] = Field("", alias="cikm18")

class DecisionMaking(BaseModel):
    """Pydantic model for Decision-Making metrics."""
    average_dm_up: Optional[str] = Field("", alias="average_dm_up")
    fintrade: Optional[str] = Field("", alias="fintrade")

class ModelMetadata(BaseModel):
    """Pydantic model for a single model's metadata."""
    model: str = Field(..., alias="model")
    average: Optional[str] = Field("", alias="average")
    type:  Optional[str] = Field("", alias="type")
    architecture:  Optional[str] = Field("", alias="architecture")
    precision:  Optional[str] = Field("", alias="precision")
    information_extraction: InformationExtraction = Field(default=InformationExtraction(), alias="information_extraction")
    textual_analysis: TextualAnalysis = Field(default=TextualAnalysis(), alias="textual_analysis")
    question_answering: QuestionAnswering = Field(default=QuestionAnswering(), alias="question_answering")
    text_generation: TextGeneration = Field(default=TextGeneration(), alias="text_generation")
    risk_management: RiskManagement = Field(default=RiskManagement(), alias="risk_management")
    forecasting: Forecasting = Field(default=Forecasting(), alias="forecasting")
    decision_making: DecisionMaking = Field(default=DecisionMaking(), alias="decision_making")

class MetadataContainer(BaseModel):
    """Pydantic model for the entire metadata container."""
    metadata: List[ModelMetadata]


def create_json_from_data(data_str: str) -> dict:
    """Converts the provided data string into the specified JSON format."""

    if not data_str.strip():
        return MetadataContainer(metadata=[ModelMetadata(model="", average="", type="", precision="", architecture="", information_extraction=InformationExtraction(), textual_analysis=TextualAnalysis(), question_answering=QuestionAnswering(), text_generation=TextGeneration(), risk_management=RiskManagement(), forecasting=Forecasting(), decision_making=DecisionMaking())]).dict()

    lines = re.split(r'🟢|⭕|🔶', data_str.strip())
    _lines = [line.strip() for line in lines if line.strip()]

    lines = [line.replace('\ n', '\n') for line in _lines]
    lines = [line.replace('\n\n', '\n') for line in _lines]

    header = lines[0].split('\n')
    header.remove('T')

    lines.remove(lines[0])
    model_data = [line.split('\n') for line in lines]

    metadata = []
    for row in model_data:
        # import pdb; pdb.set_trace()
        model_dict = dict(zip(header, row))

        # information_extraction
        information_extraction = InformationExtraction(
            average_ie_up=model_dict.get("Average IE ⬆️", ""),
            ner=model_dict.get("NER", ""),
            finer_qrd=model_dict.get("FINER-ORD", ""),
            finred=model_dict.get("FinRED", ""),
            sc=model_dict.get("SC", ""),
            cd=model_dict.get("CD", ""),
            fnxl=model_dict.get("FNXL", ""),
            fsrl=model_dict.get("FSRL", "")
        )

        # textual_analysis
        textual_analysis = TextualAnalysis(
            average_ta_up=model_dict.get("Average TA ⬆️", ""),
            fpb=model_dict.get("FPB", ""),
            fiqa_sa=model_dict.get("FiQA-SA", ""),
            headlines=model_dict.get("Headlines", ""),
            fomc=model_dict.get("FOMC", ""),
            finarg_acc=model_dict.get("FinArg-ACC", ""),
            finarg_arc=model_dict.get("FinArg-ARC", ""),
            multifin=model_dict.get("MultiFin", ""),
            ma=model_dict.get("MA", ""),
            mlesg=model_dict.get("MLESG", "")
        )

        # question_answering
        question_answering = QuestionAnswering(
            average_qa_up=model_dict.get("Average QA ⬆️", ""),
            finqa=model_dict.get("FinQA", ""),
            tatqa=model_dict.get("TATQA", ""),
            convfinqa=model_dict.get("ConvFinQA", "")
        )

        # text_generation
        text_generation = TextGeneration(
            average_tg_up=model_dict.get("Average TG ⬆️", ""),
            edtsum=model_dict.get("EDTSUM", ""),
            ectsum=model_dict.get("ECTSUM", "")
        )

        # risk_management
        risk_management = RiskManagement(
            average_rm_up=model_dict.get("Average RM ⬆️", ""),
            german=model_dict.get("German", ""),
            australian=model_dict.get("Australian", ""),
            lendingclub=model_dict.get("LendingClub", ""),
            ccf=model_dict.get("ccf", ""),
            ccfraud=model_dict.get("ccfraud", ""),
            polish=model_dict.get("polish", ""),
            taiwan=model_dict.get("taiwan", ""),
            portoseguro=model_dict.get("portoseguro", ""),
            travelinsurance=model_dict.get("travelinsurance", "")
        )

        # forecasting
        forecasting = Forecasting(
            average_fo_up=model_dict.get("Average FO ⬆️", ""),
            bigdata22=model_dict.get("BigData22", ""),
            acl18=model_dict.get("ACL18", ""),
            cikm18=model_dict.get("CIKM18", "")
        )

        # decision_making
        decision_making = DecisionMaking(
            average_dm_up=model_dict.get("Average DM ⬆️", ""),
            fintrade=model_dict.get("FinTrade", "")
        )

        metadata.append(ModelMetadata(
            model=model_dict.get("Model", ""),
            average=model_dict.get("Average ⬆️", ""),
            type=model_dict.get("Type"),
            arcbitecture=model_dict.get("Architecture"),
            precision=model_dict.get("Precision"),
            information_extraction=information_extraction,
            textual_analysis=textual_analysis,
            question_answering=question_answering,
            text_generation=text_generation,
            risk_management=risk_management,
            forecasting=forecasting,
            decision_making=decision_making
        ))
    return MetadataContainer(metadata=metadata).dict()

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


with open("finbench_leaderboard_complete_v2.json", "w") as jsonFile:
    json.dump(result_json, jsonFile)
