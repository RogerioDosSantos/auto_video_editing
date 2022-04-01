# Auto Video Editor

This project is inspired by the excellent article from *Dmytro Nikolaiev* *Automatic Video Editing using Python*. The goal of this project is to automatically cut some video fragments and then join these fragments together, as well to provide additional commands that allow you to merge different videos. 

## 

## Architecture (Components)

::: mermaid
graph LR;

%% Format

classDef c_infrastructure fill:#99ffd6,stroke:#333,stroke-width:2px;
classDef c_infrastructure_to_develop fill:#f2e6ff,stroke:#333,stroke-width:2px;
classDef c_library fill:#ffffb3,stroke:#333,stroke-width:2px;
classDef c_project_to_develop fill:#d9b3ff,stroke:#333,stroke-width:2px;
classDef c_service fill:#809fff,stroke:#333,stroke-width:2px;
classDef c_user fill:#f96,stroke:#333,stroke-width:2px;
classDef default fill:#f9f,stroke:#333,stroke-width:4px;

%% Descriptions

p_auto_video_editor_service(AI Auto Video Editor Service):::c_project_to_develop
p_onedrive(OneDrive Service):::c_service
u_video_author(Video Author):::c_user

%% Relationships

u_video_author --> p_onedrive
p_auto_video_editor_service --> p_onedrive
p_onedrive --> p_auto_video_editor_service
:::

## Workflow

::: mermaid 
sequenceDiagram 
autonumber

%% Participants
participant u_video_author as Video Author
participant p_onedrive as OneDrive Service
participant p_auto_video_editor_service as AI Auto Video Editor Service

%% Sequence

u_video_author->>p_onedrive: Login-in
activate p_onedrive 
u_video_author->>p_onedrive: Enable Service (Inform video folders and configuration)
u_video_author->>p_onedrive: Upload raw video
p_onedrive->>p_auto_video_editor_service: Request video for edition 
activate p_auto_video_editor_service 
p_auto_video_editor_service->>p_auto_video_editor_service: Download raw video and edit it
p_auto_video_editor_service->>p_onedrive: Upload edited video
deactivate p_auto_video_editor_service 
deactivate p_onedrive

:::

## More information

- [Auto Video Editor - Deck](https://microsoft-my.sharepoint-df.com/:p:/p/rogersantos/EZhAdZsxvk1At1a0rbkutjwBBbL4eFPoZmZlfl97YZEwcw?e=mCA0qd)
- [Auto Video Editor - Proposal Presentation Video](https://microsoft-my.sharepoint-df.com/:v:/p/rogersantos/EW3yiecrWONFi5yut8WA3cABd3PdmZ-aBUhF7fSqgwTLig?e=8pjIHx)
  - [Auto Video Editor - Proposal Raw Video](https://microsoft-my.sharepoint-df.com/:v:/p/rogersantos/EQvP453W7l9MvH8yJnNMZoUBWo-KcmByLqWE2PujCJ-F4w?e=bWguHA)
- [Auto Video Editor - Hackathon Demo](https://microsoft-my.sharepoint-df.com/:v:/p/rogersantos/Ea63tpt2tslOocoF6p2NL98Bw9mGDFLyCht9VbaA74j-og?e=mkgdtk)
  - [FHL Deck](https://microsoft.sharepoint.com/:p:/t/OXOOASIS/Ed3VS4XgoqdGuGtzPQcmfOABbKU0odA4yfoZWriSql0E2A?e=rAQiNi&CID=58AFF141-CF3B-4949-B6B5-1C71C19A380B&wdLOR=cF821F6F3-3BA1-4D3F-8439-4F7BD8E60395)
- [Auto Video Editor - Project Path](https://github.com/RogerioDosSantos/auto_video_editing)

## Prepare Development Machine 

Run the `./build/prepare_machine.sh`

This will install: 

- Python3: Runtime
- Pip3: Package Manager
- MoviePy Python API: Video Editor 
- Vosk Python API: Speech Recognintion

## References

- [Automatic Video Editing using Python by Dmytro Nikolaiev (Dimid)](https://towardsdatascience.com/automatic-video-editing-using-python-324e5efd7eba)
