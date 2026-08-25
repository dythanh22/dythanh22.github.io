#!/usr/bin/env python3
"""Convert remaining architecture-models groups to .qmd (AlexNet/VGG/ResNet pattern)."""

from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path("/home/iast-xeon-4/PycharmProjects/my_docs/bai-hoc/architecture-models")

GROUPS = [
    {
        "folder": "RNN",
        "group": "RNN",
        "tag": "rnn",
        "extra_cats": ["sequence"],
        "lessons": [
            ("index.md", "index.qmd", "RNN", "Tổng quan cell, unroll và BPTT", 0, "Mental model cả pipeline", "Vanilla RNN: cell, h0, forward, BPTT và vanishing gradient."),
            ("1-Single_RNN_Cell.md", "rnn-cell.qmd", "RNN Cell", None, 1, "Một bước (xt, ht−1) → ht", "Single RNN cell: hidden update từ input hiện tại và state trước."),
            ("2-Hidden_State_Initialization_.md", "hidden-init.qmd", "Hidden State Init", None, 2, "Khởi tạo h0 trước khi unroll", "Khởi tạo hidden state h0 cho chuỗi RNN."),
            ("3-Forward_Sequence_Pass.md", "forward-pass.qmd", "Forward Sequence Pass", None, 3, "Unroll theo thời gian", "Forward pass: unroll RNN trên toàn bộ sequence."),
            ("4-Backpropagation_Through_Time.md", "bptt.qmd", "BPTT", None, 4, "Lan truyền ngược qua thời gian", "Backpropagation Through Time trên RNN unroll."),
            ("5-Vanishing_Gradient_Simulation.md", "vanishing-gradient.qmd", "Vanishing Gradient", None, 5, "Chế độ vanish / explode", "Mô phỏng vanishing/exploding gradient trên RNN."),
            ("6-Complete_Vanilla_RNN.md", "complete-rnn.qmd", "Vanilla RNN hoàn chỉnh", None, 6, "Mạng đầy đủ với Why", "Lắp vanilla RNN đầu-cuối: cell, unroll, readout Why."),
        ],
    },
    {
        "folder": "LSTM",
        "group": "LSTM",
        "tag": "lstm",
        "extra_cats": ["sequence"],
        "lessons": [
            ("index.md", "index.qmd", "LSTM", "Tổng quan gate, cell state và unroll", 0, "Mental model cả pipeline", "LSTM: forget, input, cell update, output gate và mạng unroll."),
            ("1-Forget_Gate.md", "forget-gate.qmd", "Forget Gate", None, 1, "ft ⊙ Ct−1 — quên có chọn lọc", "Forget gate: quyết định thông tin cell state nào bị bỏ."),
            ("2-Input_Gate_Candidate_Memory.md", "input-gate.qmd", "Input Gate", None, 2, "it và candidate C̃t", "Input gate và candidate memory cho cập nhật LSTM."),
            ("3-Cell_State_Update.md", "cell-update.qmd", "Cell State Update", None, 3, "Cộng forget và input vào Ct", "Cập nhật cell state: Ct = ft⊙Ct−1 + it⊙C̃t."),
            ("4-Output_Gate_Hidden_State.md", "output-gate.qmd", "Output Gate", None, 4, "ht = ot ⊙ tanh(Ct)", "Output gate và hidden state từ cell state."),
            ("5-Complete_LSTM_Cell.md", "complete-cell.qmd", "LSTM Cell hoàn chỉnh", None, 5, "Ghép bốn bước thành một cell", "LSTM cell đầy đủ: forget, input, cell, output."),
            ("6-Complete_LSTM_Network.md", "complete-network.qmd", "Mạng LSTM hoàn chỉnh", None, 6, "Unroll + Wy trên chuỗi", "Mạng LSTM unroll và lớp readout."),
        ],
    },
    {
        "folder": "RNN-Encoder-Decoder-(GRU)",
        "dest_folder": "GRU",
        "group": "GRU",
        "tag": "gru",
        "extra_cats": ["sequence"],
        "lessons": [
            ("index.md", "index.qmd", "GRU", "Tổng quan encoder-decoder và các gate", 0, "Mental model cả pipeline", "GRU encoder-decoder: reset, update, candidate và seq2seq."),
            ("1-Reset_Gate.md", "reset-gate.qmd", "Reset Gate", None, 1, "rt ⊙ ht−1 trước candidate", "Reset gate GRU: kiểm soát memory cũ đưa vào candidate."),
            ("2-Update_Gate.md", "update-gate.qmd", "Update Gate", None, 2, "zt nội suy ht−1 và h̃t", "Update gate: trộn hidden cũ và candidate."),
            ("3-Candidate_Hidden_State.md", "candidate.qmd", "Candidate Hidden State", None, 3, "h̃t sau reset", "Candidate hidden state GRU từ input và reset memory."),
            ("4_Hidden-State-Update.md", "hidden-update.qmd", "Hidden State Update", None, 4, "ht = (1−zt)⊙ht−1 + zt⊙h̃t", "Cập nhật hidden GRU bằng nội suy update gate."),
            ("5-Complete_GRU_Cell.md", "complete-cell.qmd", "GRU Cell hoàn chỉnh", None, 5, "Ghép reset, update, candidate", "GRU cell đầy đủ cho một time step."),
            ("6_Complete_GRU_Network.md", "complete-network.qmd", "Mạng GRU hoàn chỉnh", None, 6, "Encoder–decoder / unroll + Wy", "Mạng GRU encoder-decoder và unroll."),
        ],
    },
    {
        "folder": "VAE",
        "group": "VAE",
        "tag": "vae",
        "extra_cats": ["generative"],
        "lessons": [
            ("index.md", "index.qmd", "VAE", "Tổng quan encoder, reparam, decoder, ELBO", 0, "Mental model cả pipeline", "VAE: encoder (μ,σ), reparameterization, decoder, KL và ELBO."),
            ("1-VAE_Encoder.md", "encoder.qmd", "VAE Encoder", None, 1, "qϕ(z|x) qua μ và log σ²", "Encoder VAE: ánh xạ input sang tham số phân phối latent."),
            ("2-Reparameterization_Trick.md", "reparameterization.qmd", "Reparameterization", None, 2, "z = μ + σ ⊙ ε", "Reparameterization trick: lấy mẫu z differentiable."),
            ("3_VAE-Decoder.md", "decoder.qmd", "VAE Decoder", None, 3, "pθ(x|z) tái tạo x̂", "Decoder VAE: sinh lại dữ liệu từ latent z."),
            ("4-KL_Divergence_Regularization.md", "kl-divergence.qmd", "KL Divergence", None, 4, "qϕ ∥ p(z) trên posterior", "KL regularization: kéo posterior về prior."),
            ("5-ELBO_Loss.md", "elbo.qmd", "ELBO", None, 5, "recon + KL", "ELBO: reconstruction loss cộng KL."),
            ("6-Complete_VAE.md", "complete-vae.qmd", "VAE hoàn chỉnh", None, 6, "Train và sample đầu-cuối", "VAE đầy đủ: encode, sample, decode, ELBO."),
        ],
    },
    {
        "folder": "GAN",
        "group": "GAN",
        "tag": "gan",
        "extra_cats": ["generative"],
        "lessons": [
            ("index.md", "index.qmd", "GAN", "Tổng quan G, D, loss và chế độ sụp", 0, "Mental model cả pipeline", "GAN: generator, discriminator, loss adversarial, train loop, mode collapse."),
            ("1-GAN_Generator.md", "generator.qmd", "Generator", None, 1, "G(z) từ noise sang mẫu", "Generator GAN: ánh xạ noise z thành mẫu tổng hợp."),
            ("2-GAN_Discriminator.md", "discriminator.qmd", "Discriminator", None, 2, "D(x) thật vs giả", "Discriminator: phân biệt dữ liệu thật và mẫu G(z)."),
            ("3-GAN_Loss_Functions.md", "loss-functions.qmd", "Hàm loss GAN", None, 3, "LD và LG", "Hàm loss minimax / non-saturating cho G và D."),
            ("4-GAN_Training_Loop.md", "training-loop.qmd", "Vòng lặp huấn luyện", None, 4, "Cập nhật D rồi G xen kẽ", "Training loop GAN: bước discriminator và generator."),
            ("5-Mode_Collapse_Detection.md", "mode-collapse.qmd", "Mode collapse", None, 5, "Phát hiện sụp mode", "Phát hiện mode collapse khi generator mất đa dạng."),
            ("6-Complete_GAN_System.md", "complete-gan.qmd", "Hệ thống GAN hoàn chỉnh", None, 6, "G + D + train đầu-cuối", "Hệ thống GAN đầy đủ: generate, discriminate, optimize."),
        ],
    },
    {
        "folder": "Word2Vec",
        "group": "Word2Vec",
        "tag": "word2vec",
        "extra_cats": ["nlp", "embeddings"],
        "lessons": [
            ("index.md", "index.qmd", "Word2Vec", "Tổng quan Skip-gram, CBOW và SGNS", 0, "Mental model cả pipeline", "Word2Vec: subsample, Skip-gram/CBOW, negative sampling, embedding."),
            ("1_Frequent_Word.md", "subsampling.qmd", "Frequent-Word Subsampling", None, 1, "Bỏ từ quá thường", "Subsampling từ frequent để cân bằng corpus Word2Vec."),
            ("2_Skip_gram.md", "skip-gram.qmd", "Skip-gram Pairs", None, 2, "(center, context) trong cửa sổ", "Sinh cặp Skip-gram từ cửa sổ ngữ cảnh."),
            ("3_Negative_Sampling.md", "negative-sampling.qmd", "Negative Sampling", None, 3, "Pn ∝ count^0.75", "Phân phối noise cho negative sampling."),
            ("4_Skip-gram_Negative.md", "sgns-loss.qmd", "SGNS Loss", None, 4, "Phân loại cặp thật vs nhiễu", "Skip-gram negative sampling loss."),
            ("5_CBOW_Forward.md", "cbow.qmd", "CBOW Forward", None, 5, "Bag of context → center", "CBOW forward: dự đoán từ trung tâm từ context."),
            ("6_SGNS_Gradient_Step.md", "sgns-gradient.qmd", "SGNS Gradient", None, 6, "Một bước SGD trên Win/Wout", "Gradient step SGNS cập nhật embedding."),
        ],
    },
    {
        "folder": "Transformer",
        "group": "Transformer",
        "tag": "transformer",
        "extra_cats": ["nlp", "attention"],
        "lessons": [
            ("index.md", "index.qmd", "Transformer", "Tổng quan encoder: embed, PE, attention, FFN", 0, "Mental model cả pipeline", "Transformer encoder: token, scale embed, PE, attention, MHA, FFN, block."),
            ("1-Word_Level_Tokenization.md", "tokenization.qmd", "Tokenization", None, 1, "Word-level token", "Word-level tokenization cho Transformer."),
            ("2-Embedding_with_Scaling.md", "embedding.qmd", "Embedding × √d", None, 2, "Embed nhân √d_model", "Embedding với scaling √d_model."),
            ("3-Sinusoidal_Positional_Encoding.md", "positional-encoding.qmd", "Positional Encoding", None, 3, "Sin/cos theo vị trí", "Sinusoidal positional encoding."),
            ("4-Scaled_Dot_Product_Attention.md", "scaled-attention.qmd", "Scaled Dot-Product Attention", None, 4, "softmax(QKᵀ/√dk) V", "Scaled dot-product attention."),
            ("5-Multi_Head_Attention.md", "multi-head.qmd", "Multi-Head Attention", None, 5, "h head song song rồi concat", "Multi-head attention."),
            ("6-Position_wise_Feed_Forward_Network.md", "ffn.qmd", "FFN", None, 6, "MLP theo vị trí token", "Position-wise feed-forward network."),
            ("7-Layer_Normalization.md", "layer-norm.qmd", "Layer Normalization", None, 7, "Chuẩn hóa trên feature token", "Layer normalization trong Transformer."),
            ("8-Transformer_Encoder_Block.md", "encoder-block.qmd", "Encoder Block", None, 8, "MHA + FFN (post-norm)", "Transformer encoder block đầy đủ."),
        ],
    },
    {
        "folder": "BERT",
        "group": "BERT",
        "tag": "bert",
        "extra_cats": ["nlp", "attention"],
        "lessons": [
            ("index.md", "index.qmd", "BERT", "Tổng quan WordPiece, MLM, NSP, pooler", 0, "Mental model cả pipeline", "BERT: WordPiece, segment, MLM, NSP, pooler và fine-tune."),
            ("1-WordPiece_Tokenization.md", "wordpiece.qmd", "WordPiece", None, 1, "Token subword BERT", "WordPiece tokenization."),
            ("2-Segment_Embeddings.md", "segment-embeddings.qmd", "Segment Embeddings", None, 2, "Etok + Epos + Eseg", "Segment embeddings cho cặp câu."),
            ("3-Masked_Language_Modeling.md", "mlm.qmd", "Masked LM", None, 3, "15% mask, 80-10-10", "Masked language modeling."),
            ("4-Next_Sentence_Prediction.md", "nsp.qmd", "Next Sentence Prediction", None, 4, "IsNext / NotNext trên [CLS]", "Next sentence prediction."),
            ("5-BERT_Pooler.md", "pooler.qmd", "BERT Pooler", None, 5, "Pooler([CLS])", "BERT pooler trên token [CLS]."),
            ("6-Fine_tuning_Architecture.md", "fine-tuning.qmd", "Fine-tuning", None, 6, "Head nhẹ trên encoder đóng băng/ft", "Kiến trúc fine-tuning BERT."),
        ],
    },
    {
        "folder": "Vision-Transformer",
        "group": "ViT",
        "tag": "vit",
        "extra_cats": ["vision", "attention"],
        "lessons": [
            ("index.md", "index.qmd", "Vision Transformer", "Tổng quan patch, CLS, encoder, head", 0, "Mental model cả pipeline", "ViT: patch embed, position, CLS, encoder Pre-LN, classification head."),
            ("1-Patch_Embedding.md", "patch-embedding.qmd", "Patch Embedding", None, 1, "Ảnh → chuỗi patch token", "Patch embedding: chiếu patch ảnh thành token."),
            ("2-Position_Embedding.md", "position-embedding.qmd", "Position Embedding", None, 2, "Cộng Epos vào patch", "Position embedding cho chuỗi patch ViT."),
            ("3-CLS_Token.md", "cls-token.qmd", "CLS Token", None, 3, "Token [CLS] làm readout", "CLS token cho phân loại ViT."),
            ("4-ViT_Encoder_Block.md", "encoder-block.qmd", "ViT Encoder Block", None, 4, "Pre-LN Transformer block", "Encoder block ViT (Pre-LN)."),
            ("5-Classification_Head.md", "classification-head.qmd", "Classification Head", None, 5, "LN + linear trên [CLS]", "Classification head ViT."),
            ("6-Complete_Vision_Transformer.md", "complete-vit.qmd", "ViT hoàn chỉnh", None, 6, "Pipeline ảnh → logits", "Vision Transformer đầu-cuối."),
        ],
    },
    {
        "folder": "UNet",
        "group": "U-Net",
        "tag": "unet",
        "extra_cats": ["vision", "segmentation"],
        "lessons": [
            ("index.md", "index.qmd", "U-Net", "Tổng quan encoder, skip, decoder, mask", 0, "Mental model cả pipeline", "U-Net: encoder, bottleneck, decoder, crop+concat skip, output mask."),
            ("1-Encoder_Block.md", "encoder-block.qmd", "Encoder Block", None, 1, "Contracting path", "Encoder block: conv + downsampling."),
            ("2-Decoder_Block.md", "decoder-block.qmd", "Decoder Block", None, 2, "Expanding path", "Decoder block: upsample + conv."),
            ("3-Skip_Connection.md", "skip-connection.qmd", "Skip Connection", None, 3, "Crop + Concat (không residual add)", "Skip U-Net: crop và concatenate encoder-decoder."),
            ("4-Bottleneck.md", "bottleneck.qmd", "Bottleneck", None, 4, "Bridge đáy chữ U", "Bottleneck (bridge) giữa encoder và decoder."),
            ("5-Output_Layer.md", "output-layer.qmd", "Lớp đầu ra", None, 5, "Conv 1×1 → mask", "Output layer: conv 1×1 ra kênh lớp."),
            ("6-Complete.md", "complete-unet.qmd", "U-Net hoàn chỉnh", None, 6, "U đầy đủ → segmentation map", "U-Net đầu-cuối cho dense prediction."),
        ],
    },
]


def strip_first_h1(body: str) -> str:
    lines = body.splitlines()
    if lines and lines[0].startswith("# "):
        lines = lines[1:]
        if lines and lines[0].strip() == "":
            lines = lines[1:]
    return "\n".join(lines).rstrip() + "\n"


def yaml_escape(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def yaml_block(lesson: tuple, group: dict, src_folder: str) -> str:
    src, _dest, title, subtitle, order, role, description = lesson
    extra = f"subtitle: {yaml_escape(subtitle)}\n" if subtitle else ""
    old_html = src.replace(".md", ".html")
    cats = ["architecture-models", "architecture", group["tag"], *group["extra_cats"]]
    cat_list = ", ".join(cats)
    aliases = [
        f"/bai-hoc/architecture-models/{src_folder}/{src}",
        f"/bai-hoc/architecture-models/{src_folder}/{old_html}",
    ]
    dest_folder = group.get("dest_folder", group["folder"])
    if dest_folder != src_folder:
        aliases.append(f"/bai-hoc/architecture-models/{dest_folder}/{src}")
        aliases.append(f"/bai-hoc/architecture-models/{dest_folder}/{old_html}")
    alias_yaml = "\n".join(f"  - {a}" for a in aliases)
    return f"""---
title: {yaml_escape(title)}
{extra}date: 2026-08-22
order: {order}
categories: [{cat_list}]
series: architecture-models
group: {yaml_escape(group["group"])}
role: {yaml_escape(role)}
description: {yaml_escape(description)}
aliases:
{alias_yaml}
---
"""


def write_metadata(dest: Path, group: dict) -> None:
    cats = ["architecture-models", "architecture", group["tag"], *group["extra_cats"]]
    cat_list = ", ".join(cats)
    dest.write_text(
        f"""group: {yaml_escape(group["group"])}
categories: [{cat_list}]
format:
  html:
    toc: true
    toc-depth: 3
    fig-align: center
""",
        encoding="utf-8",
    )


def convert_group(group: dict) -> None:
    src_folder = group["folder"]
    dest_folder = group.get("dest_folder", src_folder)
    src_base = ROOT / src_folder
    dest_base = ROOT / dest_folder
    dest_base.mkdir(exist_ok=True)

    if dest_folder != src_folder:
        src_fig = src_base / "figures"
        dest_fig = dest_base / "figures"
        if src_fig.exists() and not dest_fig.exists():
            shutil.copytree(src_fig, dest_fig)

    for lesson in group["lessons"]:
        src_name, dest_name = lesson[0], lesson[1]
        src = src_base / src_name
        if not src.exists():
            raise SystemExit(f"missing {src}")
        body = strip_first_h1(src.read_text(encoding="utf-8"))
        qmd = yaml_block(lesson, group, src_folder) + "\n" + body
        (dest_base / dest_name).write_text(qmd, encoding="utf-8")
        src.unlink()
        print(f"wrote {dest_folder}/{dest_name}")

    write_metadata(dest_base / "_metadata.yml", group)

    if dest_folder != src_folder:
        leftover = [p for p in src_base.iterdir() if p.name != "figures"]
        figs = src_base / "figures"
        if figs.exists():
            shutil.rmtree(figs)
        if leftover:
            print(f"leftover in {src_folder}: {[p.name for p in leftover]}")
        else:
            src_base.rmdir()
            print(f"removed {src_folder}")


def main() -> None:
    for group in GROUPS:
        convert_group(group)


if __name__ == "__main__":
    main()
