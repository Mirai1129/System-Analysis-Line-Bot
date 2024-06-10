def get_caregivers(domain, care_givers_data):
    care_givers_bubbles = []
    for care_giver in care_givers_data:
        bubble = {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "image",
                        "url": f"https://{domain}/static/images/caregivers/{care_giver['giver_id']}.jpg",
                        "size": "full",
                        "aspectMode": "cover",
                        "aspectRatio": "2:3",
                        "gravity": "top"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": care_giver["name"],
                                        "size": "xl",
                                        "color": "#ffffff",
                                        "weight": "bold"
                                    }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": care_giver["tag"],
                                        "color": "#ebebeb",
                                        "size": "sm",
                                        "flex": 0
                                    },
                                    {
                                        "type": "text",
                                        "text": care_giver["description"],
                                        "size": "sm",
                                        "color": "#ebebeb",
                                        "wrap": True
                                    }
                                ],
                                "spacing": "lg"
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "filler"
                                    },
                                    {
                                        "type": "box",
                                        "layout": "baseline",
                                        "contents": [
                                            {
                                                "type": "filler"
                                            },
                                            {
                                                "type": "text",
                                                "text": "🔍我想要",
                                                "color": "#ffffff",
                                                "flex": 0,
                                                "offsetTop": "-2px",
                                                "action": {
                                                    "type": "message",
                                                    "label": "action",
                                                    "text": care_giver["message_action"]
                                                }
                                            },
                                            {
                                                "type": "filler"
                                            }
                                        ],
                                        "spacing": "sm",
                                        "action": {
                                            "type": "message",
                                            "label": "action",
                                            "text": care_giver["message_action"]
                                        }
                                    },
                                    {
                                        "type": "filler"
                                    }
                                ],
                                "borderWidth": "1px",
                                "cornerRadius": "10px",
                                "spacing": "sm",
                                "borderColor": "#ffffff",
                                "margin": "xxl",
                                "height": "40px"
                            }
                        ],
                        "position": "absolute",
                        "offsetBottom": "0px",
                        "offsetStart": "0px",
                        "offsetEnd": "0px",
                        "backgroundColor": "#03303Acc",
                        "paddingAll": "20px",
                        "paddingTop": "18px"
                    }
                ],
                "paddingAll": "0px"
            }
        }
        care_givers_bubbles.append(bubble)
    return care_givers_bubbles
