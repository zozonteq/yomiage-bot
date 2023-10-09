from collections import defaultdict, deque

queue_dict = defaultdict(deque)

class guild_tts_manager:
    def __init__(self):
        pass

    def enqueue(self,voice_client, guild, source):
        queue = queue_dict[guild.id]
        queue.append(source)
        if not voice_client.is_playing():
            self.play(voice_client, queue)

    def play(self,voice_client, queue):
        if not queue or voice_client.is_playing():
            return
        source = queue.popleft()
        voice_client.play(source, after=lambda e:self.play(voice_client, queue))