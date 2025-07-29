fn recursive_analysis(context: Context) -> String 
        pass
        pass
        pass
        pass
        pass
    var result = ""
    for sub_tag in tag.sub_tags:
        result += recursive_analysis(sub_tag)
    return result + analyze_tag(tag)
