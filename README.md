# Miracom LLM Serve

## I. Getting Started

### I-1. Ollama 설치

> Ollama는 로컬에서 LLM을 쉽게 사용할 수 있도록 지원하는 플랫폼

* https://ollama.com/download 접속하여 OS 환경에 맞는 Installer 다운로드 및 설치

![mira-llm-serve-res-01](https://github.com/miracom-genai/mira-llm-serve/assets/5626425/706428b8-28f2-4c8b-b3b8-16be8f882404)

#### [Llama 2 설치 및 실행]

```shell
$ ollama run llama2
>>> Hello~
Hello! It's nice to meet you. Is there something I can help you with or
would you like to chat?

>>> Send a message (/? for help)
```

### I-2. HuggingFace GGUF 다운로드

> 💡 __HuggingFace:__ 머신러닝 커뮤니티로 모델, 데이터셋 및 응용 프로그램을 협업하는 플랫폼
>
> GGUF (GPT-Generated Unified Format)

* [yanolja/EEVE-Korean-Instruct-10.8B-v1.0](https://huggingface.co/yanolja/EEVE-Korean-Instruct-10.8B-v1.0)

#### [Huggingface CLI 설치]

```shell
$ pip install huggingface_hub
```

#### [huggingface-cli로 GGUF Download]

```shell
$ huggingface-cli download \
> heegyu/EEVE-Korean-Instruct-10.8B-v1.0-GGUF \
> ggml-model-Q5_K_M.gguf \
> --local-dir ~/ollama \
> --local-dir-use-symlinks False
Consider using `hf_transfer` for faster downloads. This solution comes with some limitations. See https://huggingface.co/docs/huggingface_hub/hf_transfer for more details.
downloading https://huggingface.co/heegyu/EEVE-Korean-Instruct-10.8B-v1.0-GGUF/resolve/main/ggml-model-Q5_K_M.gguf to /Users/julio/.cache/huggingface/hub/tmpa7nhhbgl
ggml-model-Q5_K_M.gguf:   4%|▌              | 283M/7.65G [00:22<10:05, 12.2MB/s]
```

#### [GGUF Download 사이트]

* [EEVE-Korean-Instruct-10.8B-v1.0-GGUF](https://huggingface.co/heegyu/EEVE-Korean-Instruct-10.8B-v1.0-GGUF/blob/main/ggml-model-Q5_K_M.gguf)

### I-3. 커스텀 모델 생성

#### [Modelfile 생성]

> `ggml-model-Q5_K_M.gguf` 파일을 다운로드한 위치에 생성

```txt
FROM ggml-model-Q5_K_M.gguf

TEMPLATE """{{- if .System }}
<s>{{ .System }}</s>
{{- end }}
<s>Human:
{{ .Prompt }}</s>
<s>Assistant:
"""

SYSTEM """A chat between a curious user and an artificial intelligence assistant. The assistant gives helpful, detailed, and polite answers to the user's questions."""

PARAMETER stop <s>
PARAMETER stop </s>
```

#### [Ollama Model 목록 확인]

```shell
$ ollama list
NAME         	ID          	SIZE  	MODIFIED
llama2:latest	78e26419b446	3.8 GB	2 hours ago
```

#### [Ollama Model 등록]

```shell
$ ollama create EEVE-Korean-10.8B -f ~/ollama/EEVE-Korean-Instruct-10.8B-v1.0-GGUF/Modelfile
2024/04/12 21:09:42 parser.go:73: WARN Unknown command: TEMPERATURE
transferring model data
creating model layer
creating template layer
creating system layer
creating parameters layer
creating config layer
using already created layer sha256:b9e3d1ad5e8aa6db09610d4051820f06a5257b7d7f0b06c00630e376abcfa4c1
writing layer sha256:f325fe07319c3d2716d1165b9cfa3027b1d09de996d42dbe3dc34d27df28745e
writing layer sha256:1fa69e2371b762d1882b0bd98d284f312a36c27add732016e12e52586f98a9f5
writing layer sha256:fc44d47f7d5a1b793ab68b54cdba0102140bd358739e9d78df4abf18432fb3ea
writing layer sha256:c41e9494a1e32ea2dc1ca80cc4e43a7d8bd2ff6964bbc0a811f632929aaf648d
writing manifest
success
```

#### [Ollama Model 등록 확인]

```shell
$ ollama list
NAME                    	ID          	SIZE  	MODIFIED
EEVE-Korean-10.8B:latest	338bfeec1cb8	7.7 GB	56 seconds ago
llama2:latest           	78e26419b446	3.8 GB	2 hours ago
```

#### [Ollama Model 실행]

```shell
$ ollama run EEVE-Korean-10.8B:latest
>>> Large Language Model에 대해서 한줄로 설명해주세요
대규모 언어 모델(LLM)은 방대한 양의 텍스트 데이터를 훈련시켜 인간과 유사한 방식으로 읽고, 이해하며, 응답하는 능력을 개발 기계 학습 알고리즘입니다. 이들은 자연어 처리, 생성, 번역 및 다양한 응용 분야에서 사용될 수 있습니다.
```

### I-4. LangServe 실행

#### [LangServe 필수 패키지 설치]

```shell
$ pip install -r requirements.txt
```

#### [LangServe 실행]

```shell
$ python app/server.py

INFO:     Started server process [3102]
INFO:     Waiting for application startup.

 __          ___      .__   __.   _______      _______. _______ .______     ____    ____  _______
|  |        /   \     |  \ |  |  /  _____|    /       ||   ____||   _  \    \   \  /   / |   ____|
|  |       /  ^  \    |   \|  | |  |  __     |   (----`|  |__   |  |_)  |    \   \/   /  |  |__
|  |      /  /_\  \   |  . `  | |  | |_ |     \   \    |   __|  |      /      \      /   |   __|
|  `----./  _____  \  |  |\   | |  |__| | .----)   |   |  |____ |  |\  \----.  \    /    |  |____
|_______/__/     \__\ |__| \__|  \______| |_______/    |_______|| _| `._____|   \__/     |_______|

LANGSERVE: Playground for chain "/llm/" is live at:
LANGSERVE:  │
LANGSERVE:  └──> /llm/playground/
LANGSERVE:
LANGSERVE: Playground for chain "/translate/" is live at:
LANGSERVE:  │
LANGSERVE:  └──> /translate/playground/
LANGSERVE:
LANGSERVE: Playground for chain "/prompt/" is live at:
LANGSERVE:  │
LANGSERVE:  └──> /prompt/playground/
LANGSERVE:
LANGSERVE: Playground for chain "/chat/" is live at:
LANGSERVE:  │
LANGSERVE:  └──> /chat/playground/
LANGSERVE:
LANGSERVE: See all available routes at /docs/

INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

#### [LangServe 접속]

* http://localhost:8000/prompt/playground

![mira-llm-serve-res-04](https://github.com/miracom-genai/mira-llm-serve/assets/5626425/d04c1123-bc5f-4271-a477-ee81e8e0b90d)