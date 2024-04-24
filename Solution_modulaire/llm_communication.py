from openai import OpenAI

class LLMClient:
    def __init__(self, base_url, api_key):
        """Initialise le client OpenAI avec une URL de base et une clé API."""
        self.client = OpenAI(base_url="http://localhost:4444/v1", api_key="lm-studio")
        self.history = []  # Initialisation d'une liste pour conserver l'historique des interactions

    def add_to_history(self, role, content):
        """Ajoute une interaction à l'historique."""
        self.history.append({"role": role, "content": content})

    def get_response(self, text):
        """
        Obtient une réponse du modèle LLM d'OpenAI.
        
        Args:
            text (str): Le texte de l'utilisateur pour lequel une réponse est demandée.

        Returns:
            str: La réponse générée par le modèle LLM.
        """
        # Ajout de la requête de l'utilisateur à l'historique
        self.add_to_history("user", text)

        # Ajout de la note pour le système à l'historique si nécessaire
        if len(self.history) < 2 or self.history[-2]["role"] != "system":
            self.add_to_history("system", "Tu es un assistant virtuel au service des malades atteint de neurodegenerescence. Répond de manière concise")

        # Création d'une requête de complétion avec le modèle spécifié
        completion = self.client.chat.completions.create(
            model="TheBloke/stablelm-zephyr-3b-GGUF/stablelm-zephyr-3b.Q4_K_S.gguf",
            messages=self.history,
            temperature=0.7
        )

        # Vérification si des choix sont disponibles dans la réponse
        if completion.choices:
            response = completion.choices[0].message.content
            # Sauvegarde de la réponse dans l'historique
            self.add_to_history("assistant", response)
            return response
        else:
            # Gestion du cas où aucun choix n'est disponible
            return "Pas de réponse disponible."
