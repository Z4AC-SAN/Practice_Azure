import subprocess
import requests
import json

# Configuración de tu cuenta de Jira
JIRA_URL = "https://tu-dominio.atlassian.net/rest/api/3/issue"
JIRA_USER = "tu-correo@tu-dominio.com"
JIRA_TOKEN = "tu-api-token-de-jira"

def auditar_infraestructura_azure():
    try:
        # Comando básico de Azure CLI para listar reglas de red o verificar estado
        resultado = subprocess.run(
            ["az", "network", "nsg", "rule", "list", "-g", "TuGrupoDeRecursos", "--nsg-name", "TuNSG", "--output", "json"],
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
    
    # Estructura del payload requerida por la API Cloud v3 de Jira
    payload = {
        "fields": {
            "project": {
                "key": "IT"  # Cambia por la clave corta de tu proyecto en Jira (ej. ITSM, PROJ)
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
                "name": "Task"  # Puede ser "Task", "Bug" o "Incident" según tu configuración de Jira
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