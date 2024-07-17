from app.src.core.models.types.orquestrador_message_adapter import OrquestradorMessageAdapter

class SQSMessageAdapter():
    @staticmethod
    def adapt(message: dict) -> OrquestradorMessageAdapter:
        try:
            return {
                "TableName": message.get("nome_tabela"),
                "DatabaseName": message.get("nome_database"),
                "Partitions": message.get("partições"),
                "StepFunctionID": message.get("id_da_stepfuncion_anterior")
            }
        except KeyError as error:
            raise KeyError(f"Chave ausente na mensagem de entrada: {str(error)}") from error
        
#talvez tenha que lançar erro se chegar uma mensagem mal formatada
#mas seguir o codigo e de alguma forma reportar essa quebra