     struct CognitiveProcess:
         var tags: List[Tag]

         fn add_tag(tag: Tag):
             self.tags.append(tag)