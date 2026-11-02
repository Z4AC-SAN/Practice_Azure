import subprocess
import requests
import json

# ==============================================================================
# CONFIGURACIÓN INICIAL: Modifica únicamente estos valores con tus datos
# ==============================================================================
JIRA_DOMINIO = "tu-dominio"                  # Ej: alumno-team-xxxxx (sin .atlassian.net)
JIRA_USER = "tu-correo@dominio.com"          # Tu correo de registro en Atlassian
JIRA_TOKEN = "tu-token-de-api-aqui"          # Tu Token de Acceso Personal (PAT) de Jira
JIRA_PROJECT_KEY = "IT"                      # Clave corta de tu proyecto (ej. IT, PROJ)

AZURE_RESOURCE_GROUP = "TuGrupoDeRecursos"     # Nombre de tu Grupo de Recursos en Azure
AZURE_NSG_NAME = "TuNSG"                     # Nombre de tu Network Security Group
# ==============================================================================

# Construcción automática de la URL de la API de Jira
JIRA_URL = f"https://{JIRA_DOMINIO}.atlassian.net/rest/api/3/issue"

def auditar_infraestructura_azure():
    try:
        # Comando de Azure CLI utilizando las variables configuradas arriba
        resultado = subprocess.run(
            ["az", "network", "nsg", "rule", "list", "-g", AZURE_RESOURCE_GROUP, "--nsg-name", AZURE_NSG_NAME, "--output", "json"],
            capture_output=True,
            text=True,
            check=True
        )
        reglas = json.loads(resultado.stdout)
        return f"Auditoría completada con éxito. Total de reglas de red evaluadas: {len(reglas)}."
    except Exception as e:
        return f"Incidente detectado: Fallo en la consulta a la infraestructura de Azure. Detalle: {str(e)}"

def crear_ticket_jira(detalle_incidencia):
    auth = (JIRA_USER, JIRA_TOKEN)
    headers = {"Content-Type": "application/json"}
    
    # Payload estructurado para la API Cloud v3 de Jira
    payload = {
        "fields": {
            "project": {
                "key": JIRA_PROJECT_KEY
            },
            "summary": "INC-NET-01: Revisión automática requerida en infraestructura de red",
            "description": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {
                                "type": "text",
                                "text": f"El agente automatizado ha generado esta alerta técnica:\n\n{detalle_incidencia}\n\nAcción requerida: Un operador humano debe revisar y resolver la incidencia."
                            }
                        ]
                    }
                ]
            },
            "issuetype": {
                "name": "Task"
            }
        }
    }
    
    response = requests.post(JIRA_URL, json=payload, headers=headers, auth=auth)
    
    if response.status_code == 201:
        print("¡Ticket creado exitosamente en Jira! Queda disponible para que alguien lo resuelva.")
    else:
        print(f"Error al crear el ticket en Jira: {response.status_code} - {response.text}")

if __name__ == "__main__":
    print("Iniciando ejecución del Agente ITIL...")
    informacion_incidencia = auditar_infraestructura_azure()
    crear_ticket_jira(informacion_incidencia)