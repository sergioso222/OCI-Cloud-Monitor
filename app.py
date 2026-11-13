import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import oci

load_dotenv()

app = Flask(__name__)

# Configuración segura de OCI desde .env
oci_config = {
    "user": os.getenv("OCI_USER_OCID"),
    "key_file": os.getenv("OCI_KEY_FILE"),
    "fingerprint": os.getenv("OCI_FINGERPRINT"),
    "tenancy": os.getenv("OCI_TENANCY_OCID"),
    "region": os.getenv("OCI_REGION"),
}

COMPARTMENT_ID = os.getenv("OCI_COMPARTMENT_ID")


def get_oci_instances():
    """Consulta las instancias de Compute y sus IPs públicas/privadas en OCI."""
    compute_client = oci.core.ComputeClient(oci_config)
    network_client = oci.core.VirtualNetworkClient(oci_config)

    instances_response = compute_client.list_instances(compartment_id=COMPARTMENT_ID)
    instances_data = []

    for inst in instances_response.data:
        public_ip = "N/A"
        private_ip = "N/A"

        vnic_attachments = compute_client.list_vnic_attachments(
            compartment_id=COMPARTMENT_ID,
            instance_id=inst.id
        ).data

        for attachment in vnic_attachments:
            if attachment.lifecycle_state == "ATTACHED":
                vnic = network_client.get_vnic(attachment.vnic_id).data
                private_ip = vnic.private_ip or "N/A"
                public_ip = vnic.public_ip or "Sin IP pública"
                break

        instances_data.append({
            "name": inst.display_name,
            "state": inst.lifecycle_state,
            "shape": inst.shape,
            "region": inst.region,
            "private_ip": private_ip,
            "public_ip": public_ip,
            "time_created": inst.time_created.strftime("%Y-%m-%d %H:%M")
        })

    return instances_data


def analyze_sentiment_oci(text):
    """Consume OCI AI Language para analizar el sentimiento de un texto."""
    ai_client = oci.ai_language.AIServiceLanguageClient(oci_config)

    document = oci.ai_language.models.TextDocument(
        key="doc_1",
        text=text
    )

    details = oci.ai_language.models.BatchDetectLanguageSentimentsDetails(
        documents=[document]
    )

    response = ai_client.batch_detect_language_sentiments(
        batch_detect_language_sentiments_details=details,
        level=["ASPECT", "SENTENCE"]
    )

    result_doc = response.data.documents[0]

    aspects = [
        {
            "text": asp.text,
            "sentiment": asp.sentiment,
            "scores": asp.scores
        }
        for asp in (result_doc.aspects or [])
    ]

    return {
        "sentiment": result_doc.document_sentiment,
        "scores": result_doc.document_scores,
        "aspects": aspects
    }


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/instances")
def api_instances():
    try:
        data = get_oci_instances()
        return jsonify({"status": "ok", "instances": data})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/api/sentiment", methods=["POST"])
def api_sentiment():
    data = request.get_json() or {}
    text = data.get("text", "").strip()

    if not text:
        return jsonify({"status": "error", "message": "Por favor escribe un texto para analizar."}), 400

    try:
        analysis = analyze_sentiment_oci(text)
        return jsonify({"status": "ok", "result": analysis})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)