import os
from typing import Optional
from backend.youtube_growth import (
    get_channel,
    list_channels,
    analyze_topic_opportunities,
    detect_content_opportunities,
)
from backend.youtube_pattern_analyzer import (
    analyze_channel,
)
from backend.youtube_hook_retention import (
    hook_retention_intelligence,
)
from backend.youtube_title_intelligence import (
    title_intelligence,
)
from backend.youtube_thumbnail_intelligence import (
    thumbnail_intelligence,
)
from backend.youtube_script_optimizer import (
    script_optimizer,
)
from backend.youtube_seo_engine import (
    seo_engine,
)
from backend.youtube_experiment_engine import (
    experiment_engine,
)
from backend.youtube_post_publish_analytics import (
    post_publish_analytics,
)
from backend.youtube_self_learning import (
    self_learning,
)
class YouTubeAutopilot:
    def channel_overview(
        self,
        channel_id: Optional[str] = None,
    ):
        if channel_id:
            channel = get_channel(channel_id)
        else:
            channels = list_channels()
            channel = (
                channels[0]
                if channels
                else None
            )
        if not channel:
            return {
                "success": False,
                "error": "Channel not found",
            }
        return {
            "success": True,
            "channel": channel,
        }
    def intelligence_overview(
        self,
        channel_id: Optional[str] = None,
    ):
        overview = self.channel_overview(
            channel_id
        )
        if not overview["success"]:
            return overview
        channel = overview["channel"]
        channel_db_id = channel.get("id")
        if channel_db_id is None:
            return {
                "success": False,
                "error": "Channel database ID not found",
            }
        pattern = analyze_channel(
            channel_db_id
        )
        topics = analyze_topic_opportunities()
        opportunities = detect_content_opportunities(channel_id=channel["channel_id"])
        hooks = hook_retention_intelligence.analyze(channel_id=channel["channel_id"])
        titles = title_intelligence.analyze_channel(channel["channel_id"])
        thumbnails = thumbnail_intelligence.analyze_channel(channel["channel_id"])
        learning = self_learning.summary()
        return {
            "success": True,
            "channel": channel,
            "pattern_analysis": pattern,
            "topic_opportunities": topics,
            "content_opportunities": opportunities,
            "hook_retention": hooks,
            "title_intelligence": titles,
            "thumbnail_intelligence": thumbnails,
            "learning_summary": learning,
        }
    def private_analytics(
        self,
        channel_id: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ):
        from datetime import date, timedelta
        from backend.youtube_analytics import youtube_analytics
        from backend.youtube_oauth import youtube_oauth
        # Refresh the persisted Google OAuth token after backend restart.
        access_token = getattr(
            youtube_oauth,
            "access_token",
            None,
        )
        if not access_token:
            refresh_result = (
                youtube_oauth.refresh_access_token()
            )
            if not refresh_result.get("success"):
                return {
                    "success": False,
                    "authorized": False,
                    "private_metrics": True,
                    "metrics": {},
                    "error": refresh_result.get(
                        "error",
                        "YouTube Analytics OAuth refresh failed.",
                    ),
                }
            access_token = getattr(
                youtube_oauth,
                "access_token",
                None,
            )
        if access_token:
            youtube_analytics.configure_access_token(
                access_token
            )
        resolved_channel_id = (
            channel_id
            or os.getenv(
                "YOUTUBE_CHANNEL_ID",
                "UCP75FPRq4DaMoe88G9R3heg",
            )
        ).strip()
        if not start_date:
            start_date = (
                date.today() - timedelta(days=28)
            ).isoformat()
        if not end_date:
            end_date = date.today().isoformat()
        result = youtube_analytics.get_channel_metrics(
            start_date=start_date,
            end_date=end_date,
        )
        result["channel_id"] = resolved_channel_id
        result["source"] = "YouTube Analytics API"
        result["private_metrics"] = True
        result["date_range"] = {
            "start_date": start_date,
            "end_date": end_date,
        }
        return result
    def intelligence_with_analytics(
        self,
        channel_id: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ):
        """
        Combine existing YouTube Intelligence with verified
        private YouTube Analytics.
        Existing intelligence is preserved. Private analytics is
        added as a separate verified source.
        """
        intelligence = self.intelligence_overview(
            channel_id=channel_id,
        )
        analytics = self.private_analytics(
            channel_id=channel_id,
            start_date=start_date,
            end_date=end_date,
        )
        return {
            "success": bool(
                intelligence.get("success")
                and analytics.get("success")
            ),
            "channel": intelligence.get("channel"),
            "youtube_intelligence": intelligence,
            "private_analytics": analytics,
            "analytics_verified": bool(
                analytics.get("success")
                and analytics.get("private_metrics")
            ),
        }
    def performance_recommendations(
        self,
        channel_id: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ):
        """
        Generate performance-based recommendation signals from
        verified private Analytics + existing YouTube Intelligence.
        No private metric is invented. Recommendations are derived
        only from the returned verified data and existing intelligence.
        """
        combined = self.intelligence_with_analytics(
            channel_id=channel_id,
            start_date=start_date,
            end_date=end_date,
        )
        if not combined.get("success"):
            return {
                "success": False,
                "error": combined.get(
                    "error",
                    "Combined YouTube intelligence unavailable.",
                ),
                "source": "YouTube Intelligence + YouTube Analytics API",
            }
        analytics = combined.get(
            "private_analytics",
            {},
        )
        metrics = analytics.get(
            "metrics",
            {},
        )
        views = metrics.get("views")
        likes = metrics.get("likes")
        comments = metrics.get("comments")
        avg_duration = metrics.get(
            "average_view_duration_seconds"
        )
        avg_percentage = metrics.get(
            "average_percentage_viewed"
        )
        subscribers_gained = metrics.get(
            "subscribers_gained"
        )
        signals = []
        if isinstance(avg_percentage, (int, float)):
            if avg_percentage >= 60:
                signals.append({
                    "area": "retention",
                    "signal": "strong",
                    "evidence": {
                        "average_percentage_viewed": avg_percentage,
                    },
                    "recommendation": (
                        "Keep the current short-form pacing and "
                        "test new Shorts using similarly direct hooks."
                    ),
                })
            elif avg_percentage >= 40:
                signals.append({
                    "area": "retention",
                    "signal": "moderate",
                    "evidence": {
                        "average_percentage_viewed": avg_percentage,
                    },
                    "recommendation": (
                        "Test a faster opening and reduce unnecessary "
                        "setup before the main joke or payoff."
                    ),
                })
            else:
                signals.append({
                    "area": "retention",
                    "signal": "needs_attention",
                    "evidence": {
                        "average_percentage_viewed": avg_percentage,
                    },
                    "recommendation": (
                        "Prioritize stronger first-seconds hooks and "
                        "shorter setup before the main payoff."
                    ),
                })
        if (
            isinstance(views, (int, float))
            and isinstance(likes, (int, float))
            and views > 0
        ):
            like_rate = (likes / views) * 100
            signals.append({
                "area": "engagement",
                "signal": "measured",
                "evidence": {
                    "views": views,
                    "likes": likes,
                    "like_rate_percent": round(
                        like_rate,
                        2,
                    ),
                },
                "recommendation": (
                    "Use the measured engagement rate as a baseline "
                    "when evaluating future Shorts."
                ),
            })
        if (
            isinstance(comments, (int, float))
            and isinstance(views, (int, float))
            and views > 0
        ):
            comment_rate = (comments / views) * 100
            signals.append({
                "area": "comments",
                "signal": "measured",
                "evidence": {
                    "views": views,
                    "comments": comments,
                    "comment_rate_percent": round(
                        comment_rate,
                        2,
                    ),
                },
                "recommendation": (
                    "Test stronger comment prompts and simple "
                    "viewer-choice questions in future Shorts."
                ),
            })
        if isinstance(subscribers_gained, (int, float)):
            signals.append({
                "area": "subscriber_conversion",
                "signal": "measured",
                "evidence": {
                    "subscribers_gained": subscribers_gained,
                },
                "recommendation": (
                    "Track subscriber gain alongside views when "
                    "evaluating future content."
                ),
            })
        intelligence = combined.get(
            "youtube_intelligence",
            {},
        )
        return {
            "success": True,
            "channel": combined.get("channel"),
            "date_range": analytics.get("date_range"),
            "analytics_verified": combined.get(
                "analytics_verified",
                False,
            ),
            "private_metrics": metrics,
            "performance_signals": signals,
            "youtube_intelligence": intelligence,
            "recommendation_basis": [
                "verified private YouTube Analytics",
                "existing YouTube Intelligence",
                "historical channel data",
            ],
        }
    def next_shorts_plan(
        self,
        channel_id: Optional[str] = None,
        title: Optional[str] = None,
    ):
        """
        Convert verified performance recommendations into a
        concrete next-Shorts planning package.
        Existing plan_video and experiment systems remain untouched.
        """
        recommendations = self.performance_recommendations(
            channel_id=channel_id,
        )
        if not recommendations.get("success"):
            return {
                "success": False,
                "error": recommendations.get(
                    "error",
                    "Performance recommendations unavailable.",
                ),
            }
        signals = recommendations.get(
            "performance_signals",
            [],
        )
        retention_signal = next(
            (
                item
                for item in signals
                if item.get("area") == "retention"
            ),
            {},
        )
        if retention_signal.get("signal") == "strong":
            hook = (
                "????? ??? ????????? ???? ???? ?? surprise ?????"
            )
            pacing = (
                "????? pacing ????? ??? unnecessary setup ????"
            )
        else:
            hook = (
                "????? ??? ???????? strong curiosity hook ???"
            )
            pacing = (
                "????? setup ? joke ? payoff structure ??????? ????"
            )
        selected_title = (
            title
            or "?? ????? ????????? ??? ???? ????? ????? ?? ???! ??"
        )
        plan = self.plan_video(
            title=selected_title,
            topic="Bangla Comedy Shorts ? Village Comedy",
            video_format="shorts",
        )
        experiment = self.experiment_plan(
            title=selected_title,
            thumbnail_concept=(
                "???? exaggerated funny reaction + "
                "?? ??? ?????? ????? text"
            ),
        )
        return {
            "success": True,
            "channel": recommendations.get("channel"),
            "date_range": recommendations.get("date_range"),
            "analytics_verified": recommendations.get(
                "analytics_verified",
                False,
            ),
            "performance_signals": signals,
            "next_shorts": {
                "title": selected_title,
                "topic": "Bangla Comedy Shorts ? Village Comedy",
                "format": "shorts",
                "hook": hook,
                "pacing": pacing,
                "structure": [
                    "0?2 sec: Hook",
                    "2?10 sec: Setup",
                    "10?25 sec: Main comedy/action",
                    "25?35 sec: Payoff",
                    "Final seconds: Short CTA",
                ],
                "thumbnail_concept": (
                    "???? facial reaction + "
                    "???? clear action moment + "
                    "?? ??? ?????? text"
                ),
            },
            "video_plan": plan,
            "experiment_plan": experiment,
            "source": [
                "verified private YouTube Analytics",
                "existing YouTube Intelligence",
                "performance recommendations",
            ],
        }
    def next_shorts_script(
        self,
        channel_id: Optional[str] = None,
    ):
        """
        Convert the verified next-Shorts plan into a concrete
        script brief.
        The script brief is derived from:
        - verified private YouTube Analytics
        - existing YouTube Intelligence
        - performance recommendations
        - the next Shorts plan
        No private metric is invented.
        """
        plan = self.next_shorts_plan(
            channel_id=channel_id,
        )
        if not plan.get("success"):
            return {
                "success": False,
                "error": plan.get(
                    "error",
                    "Verified next Shorts plan unavailable.",
                ),
                "source": "YouTube Intelligence + YouTube Analytics API",
            }
        next_shorts = plan.get("next_shorts", {})
        retention_signal = "moderate"
        for signal in plan.get("performance_signals", []):
            if signal.get("area") == "retention":
                retention_signal = signal.get(
                    "signal",
                    "moderate",
                )
                break
        if retention_signal == "strong":
            opening_style = (
                "Start immediately with the funny situation; "
                "avoid a long introduction."
            )
            pacing = "Fast pacing with the main joke introduced in the first seconds."
        elif retention_signal == "needs_attention":
            opening_style = (
                "Open with the strongest funny moment or surprising line "
                "before giving any setup."
            )
            pacing = "Very fast pacing with minimal setup and quick payoff."
        else:
            opening_style = (
                "Open directly with the situation and a clear curiosity hook."
            )
            pacing = "Fast pacing with short setup and an early payoff."
        script = {
            "language": "bn",
            "format": "shorts",
            "title": next_shorts.get("title"),
            "topic": next_shorts.get("topic"),
            "hook": next_shorts.get("hook"),
            "opening_style": opening_style,
            "pacing": pacing,
            "duration_target": "20-35 seconds",
            "structure": [
                {
                    "part": "hook",
                    "duration": "0-3s",
                    "instruction": (
                        "Begin with the strongest curiosity or comedy hook."
                    ),
                },
                {
                    "part": "setup",
                    "duration": "3-8s",
                    "instruction": (
                        "Show the situation quickly without unnecessary explanation."
                    ),
                },
                {
                    "part": "escalation",
                    "duration": "8-20s",
                    "instruction": (
                        "Increase the comedy through action, reaction, "
                        "or an unexpected mistake."
                    ),
                },
                {
                    "part": "payoff",
                    "duration": "20-30s",
                    "instruction": (
                        "Deliver the main funny payoff clearly and quickly."
                    ),
                },
                {
                    "part": "cta",
                    "duration": "final 2-3s",
                    "instruction": (
                        "Use a short natural comment/like prompt without "
                        "interrupting the comedy."
                    ),
                },
            ],
            "thumbnail_concept": next_shorts.get(
                "thumbnail_concept"
            ),
            "verified_analytics": plan.get(
                "analytics_verified",
                False,
            ),
            "date_range": plan.get("date_range"),
            "performance_signals": plan.get(
                "performance_signals",
                [],
            ),
            "source": [
                "verified private YouTube Analytics",
                "existing YouTube Intelligence",
                "performance recommendations",
                "next Shorts plan",
            ],
        }
        return {
            "success": True,
            "channel": plan.get("channel"),
            "date_range": plan.get("date_range"),
            "analytics_verified": plan.get(
                "analytics_verified",
                False,
            ),
            "next_shorts": next_shorts,
            "script": script,
            "source": [
                "verified private YouTube Analytics",
                "existing YouTube Intelligence",
                "performance recommendations",
                "next Shorts plan",
            ],
        }
    def next_shorts_seo(
        self,
        channel_id: Optional[str] = None,
    ):
        """
        Generate a concrete SEO package from the verified
        next Shorts script plan.
        No private Analytics metric is invented.
        """
        script_result = self.next_shorts_script(
            channel_id=channel_id,
        )
        if not script_result.get("success"):
            return {
                "success": False,
                "error": script_result.get(
                    "error",
                    "Verified Shorts script unavailable.",
                ),
            }
        script = script_result.get("script", {})
        title = script.get("title") or "Bangla Comedy Shorts ??"
        topic = script.get("topic") or "Bangla Comedy Shorts"
        seo = {
            "title": title,
            "description": (
                f"{title}\n\n"
                "????? ??????? ????? ???? ???? Bangla Comedy Shorts! "
                "??? ??????? ????? ??? ????? ????? ??????? ?????? "
                "??????? ???? ????? Like, Comment ??? Subscribe ?????\n\n"
                "#Shorts #BanglaComedy #FunnyVideo"
            ),
            "tags": [
                "bangla comedy",
                "bangla funny video",
                "bangla shorts",
                "funny bangla shorts",
                "bangladesh comedy",
                "bangladesh shorts",
                "village comedy",
                "village funny video",
                "bangla funny shorts",
                "comedy shorts",
                "funny video",
                "The Ismail Jr",
                "ismail jr",
                "????? ?????",
                "????? ?????",
                "???? ?????",
                "???? ?????",
                "??????? ?????",
            ],
            "hashtags": [
                "#Shorts",
                "#BanglaComedy",
                "#BanglaShorts",
                "#FunnyVideo",
                "#VillageComedy",
                "#TheIsmailJr",
            ],
            "keywords": [
                "Bangla comedy Shorts",
                "Bangla funny video",
                "Bangladesh comedy",
                "village comedy",
                "funny Bangla Shorts",
                "????? ?????",
                "????? ???? ?????",
                "????? ?????",
            ],
            "cta": (
                "??????? ???? ????? Like ???, "
                "??????? ????? ????? ????? ??? Subscribe ?????"
            ),
            "topic": topic,
            "source": [
                "verified private YouTube Analytics",
                "existing YouTube Intelligence",
                "performance recommendations",
                "next Shorts plan",
                "next Shorts script",
            ],
        }
        return {
            "success": True,
            "channel": script_result.get("channel"),
            "date_range": script_result.get("date_range"),
            "analytics_verified": script_result.get(
                "analytics_verified",
                False,
            ),
            "seo": seo,
            "script": script,
            "source": seo["source"],
        }
    def next_shorts_thumbnail_package(
        self,
        channel_id: Optional[str] = None,
    ):
        """
        Combine verified Shorts SEO with existing
        YouTube Thumbnail Intelligence.
        No private Analytics metric is invented.
        """
        seo_result = self.next_shorts_seo(
            channel_id=channel_id,
        )
        if not seo_result.get("success"):
            return {
                "success": False,
                "error": seo_result.get(
                    "error",
                    "Verified Shorts SEO unavailable.",
                ),
            }
        channel = seo_result.get("channel")
        seo = seo_result.get("seo", {})
        topic = seo.get("topic") or "Bangla Comedy Shorts"
        # Existing Thumbnail Intelligence
        thumbnail_intelligence = None
        try:
            thumbnail_intelligence = self.thumbnail_intelligence(
                channel_id=channel_id,
            )
        except TypeError:
            try:
                thumbnail_intelligence = self.thumbnail_intelligence()
            except Exception as exc:
                thumbnail_intelligence = {
                    "success": False,
                    "error": str(exc),
                }
        except Exception as exc:
            thumbnail_intelligence = {
                "success": False,
                "error": str(exc),
            }
        if not isinstance(thumbnail_intelligence, dict):
            thumbnail_intelligence = {
                "success": False,
                "error": "Thumbnail Intelligence returned an invalid result.",
            }
        # Preserve the existing intelligence result.
        thumbnail_source = thumbnail_intelligence.get(
            "recommendations"
        )
        if not thumbnail_source:
            thumbnail_source = thumbnail_intelligence.get(
                "thumbnail_recommendations"
            )
        if not thumbnail_source:
            thumbnail_source = thumbnail_intelligence.get(
                "patterns"
            )
        if not thumbnail_source:
            thumbnail_source = []
        package = {
            "title": seo.get("title"),
            "topic": topic,
            "thumbnail": {
                "thumbnail_text": "?? ??? ????! ??",
                "visual_focus": (
                    "?????? ?????? ???? reaction moment-?? "
                    "thumbnail-?? ??? focus ?????"
                ),
                "face_expression": (
                    "?? surprise/funny expression, "
                    "??? ? ??? clearly visible?"
                ),
                "composition": (
                    "?? ???? expressive face, ???? ???? "
                    "??? funny object/action; background simple ??????"
                ),
                "text_style": (
                    "????? ?? ????? ????, ?????? ???????? "
                    "???? ??? ??? ??? ???????? text?"
                ),
                "background": (
                    "?????? real scene ??????? ???? ??? "
                    "?????????? background elements ?? ??????"
                ),
                "thumbnail_concept": (
                    "Funny reaction + unexpected action + "
                    "???? ?? curiosity element?"
                ),
            },
            "seo": seo,
            "existing_thumbnail_intelligence": thumbnail_intelligence,
            "thumbnail_intelligence_data": thumbnail_source,
            "analytics_verified": seo_result.get(
                "analytics_verified",
                False,
            ),
            "date_range": seo_result.get("date_range"),
            "source": [
                "verified private YouTube Analytics",
                "existing YouTube Intelligence",
                "existing Thumbnail Intelligence",
                "performance recommendations",
                "next Shorts plan",
                "next Shorts script",
                "next Shorts SEO",
            ],
        }
        return {
            "success": True,
            "channel": channel,
            "date_range": seo_result.get("date_range"),
            "analytics_verified": seo_result.get(
                "analytics_verified",
                False,
            ),
            "thumbnail_package": package,
            "source": package["source"],
        }
    def final_shorts_package(
        self,
        channel_id: Optional[str] = None,
    ):
        """
        Combine the verified Shorts script, SEO, thumbnail
        intelligence and private Analytics into one final
        ready-to-use content package.
        No private Analytics metric is invented.
        """
        script_result = self.next_shorts_script(
            channel_id=channel_id,
        )
        seo_result = self.next_shorts_seo(
            channel_id=channel_id,
        )
        thumbnail_result = self.next_shorts_thumbnail_package(
            channel_id=channel_id,
        )
        if not script_result.get("success"):
            return {
                "success": False,
                "error": script_result.get(
                    "error",
                    "Verified Shorts script unavailable.",
                ),
            }
        if not seo_result.get("success"):
            return {
                "success": False,
                "error": seo_result.get(
                    "error",
                    "Verified Shorts SEO unavailable.",
                ),
            }
        if not thumbnail_result.get("success"):
            return {
                "success": False,
                "error": thumbnail_result.get(
                    "error",
                    "Verified Shorts thumbnail package unavailable.",
                ),
            }
        script = script_result.get("script", {})
        seo = seo_result.get("seo", {})
        thumbnail_package = thumbnail_result.get(
            "thumbnail_package",
            {},
        )
        thumbnail = thumbnail_package.get(
            "thumbnail",
            {},
        )
        return {
            "success": True,
            "channel": script_result.get("channel"),
            "date_range": script_result.get("date_range"),
            "analytics_verified": bool(
                script_result.get("analytics_verified")
                and seo_result.get("analytics_verified")
                and thumbnail_result.get("analytics_verified")
            ),
            "final_shorts_package": {
                "title": seo.get("title") or script.get("title"),
                "topic": script.get("topic"),
                "format": script.get("format", "shorts"),
                "language": script.get("language", "bn"),
                "script": script,
                "seo": {
                    "description": seo.get("description"),
                    "tags": seo.get("tags", []),
                    "hashtags": seo.get("hashtags", []),
                    "keywords": seo.get("keywords", []),
                    "cta": seo.get("cta"),
                },
                "thumbnail": {
                    "thumbnail_text": thumbnail.get(
                        "thumbnail_text"
                    ),
                    "visual_focus": thumbnail.get(
                        "visual_focus"
                    ),
                    "face_expression": thumbnail.get(
                        "face_expression"
                    ),
                    "composition": thumbnail.get(
                        "composition"
                    ),
                    "text_style": thumbnail.get(
                        "text_style"
                    ),
                    "background": thumbnail.get(
                        "background"
                    ),
                    "thumbnail_concept": thumbnail.get(
                        "thumbnail_concept"
                    ),
                },
                "pacing": script.get("pacing"),
                "duration_target": script.get(
                    "duration_target"
                ),
                "structure": script.get("structure"),
                "performance_signals": script_result.get(
                    "performance_signals",
                    [],
                ),
            },
            "source": [
                "verified private YouTube Analytics",
                "existing YouTube Intelligence",
                "performance recommendations",
                "next Shorts plan",
                "next Shorts script",
                "next Shorts SEO",
                "existing Thumbnail Intelligence",
                "next Shorts thumbnail package",
            ],
        }
    def plan_video(
        self,
        title: str,
        topic: Optional[str] = None,
        video_format: str = "shorts",
        script: Optional[str] = None,
        thumbnail_concept: Optional[str] = None,
    ):
        title_result = title_intelligence.analyze(
            title
        )
        thumbnail_result = (
            thumbnail_intelligence.analyze(
                thumbnail_concept
                or title
            )
        )
        script_result = None
        if script:
            script_result = script_optimizer.analyze(
                script
            )
        seo_result = seo_engine.package(title=title, topic=topic or "")
        structure = script_optimizer.generate_structure(
            video_format
        )
        return {
            "success": True,
            "video_plan": {
                "title": title,
                "topic": topic,
                "format": video_format,
                "title_analysis": title_result,
                "thumbnail_analysis": thumbnail_result,
                "script_analysis": script_result,
                "script_structure": structure,
                "seo_package": seo_result,
            },
        }
    def experiment_plan(
        self,
        title: str,
        thumbnail_concept: Optional[str] = None,
        hook: Optional[str] = None,
    ):
        variants = experiment_engine.create_variants(
            "title",
            [
                title,
                f"{title} 😂",
                f"আপনি এটা জানেন? {title}",
            ],
        )
        thumbnail_variants = experiment_engine.create_variants(
            "thumbnail",
            [
                thumbnail_concept or title,
                f"BIG REACTION: {thumbnail_concept or title}",
                f"SHOCK: {thumbnail_concept or title}",
            ],
        )
        return {
            "success": True,
            "title_variants": variants,
            "thumbnail_variants": thumbnail_variants,
            "hook": hook,
        }
    def post_publish(
        self,
        video_id: int,
    ):
        return post_publish_analytics.analyze_video(
            video_id
        )
    def learn(
        self,
        channel_db_id: int,
    ):
        return self_learning.learn(
            channel_db_id
        )
    def command(
        self,
        action: str,
        channel_id: Optional[str] = None,
        channel_db_id: Optional[int] = None,
        title: Optional[str] = None,
        topic: Optional[str] = None,
        video_format: str = "shorts",
        script: Optional[str] = None,
        thumbnail_concept: Optional[str] = None,
        video_id: Optional[int] = None,
    ):
        action = str(
            action or ""
        ).strip().lower()
        if action in {
            "overview",
            "analyze",
            "intelligence",
        }:
            return self.intelligence_overview(
                channel_id
            )
        if action in {
            "plan",
            "plan_video",
            "create_plan",
        }:
            if not title:
                return {
                    "success": False,
                    "error": "title is required",
                }
            return self.plan_video(
                title=title,
                topic=topic,
                video_format=video_format,
                script=script,
                thumbnail_concept=thumbnail_concept,
            )
        if action in {
            "experiment",
            "experiments",
            "ab_test",
        }:
            if not title:
                return {
                    "success": False,
                    "error": "title is required",
                }
            return self.experiment_plan(
                title=title,
                thumbnail_concept=thumbnail_concept,
            )
        if action in {
            "private_analytics",
            "channel_analytics",
            "youtube_analytics",
        }:
            return self.private_analytics(
                channel_id=channel_id,
            )
        if action in {
            "final_shorts_package",
            "complete_shorts_package",
            "youtube_shorts_package",
        }:
            return self.final_shorts_package(
                channel_id=channel_id,
            )
        if action in {
            "next_shorts_thumbnail_package",
            "shorts_thumbnail_package",
            "generate_thumbnail_package",
        }:
            return self.next_shorts_thumbnail_package(
                channel_id=channel_id,
            )
        if action in {
            "next_shorts_seo",
            "shorts_seo",
            "generate_shorts_seo",
        }:
            return self.next_shorts_seo(
                channel_id=channel_id,
            )
        if action in {
            "next_shorts_script",
            "shorts_script",
            "generate_shorts_script",
        }:
            return self.next_shorts_script(
                channel_id=channel_id,
            )
        if action in {
            "next_shorts_plan",
            "next_video_plan",
            "recommend_next_shorts",
        }:
            return self.next_shorts_plan(
                channel_id=channel_id,
            )
        if action in {
            "performance_recommendations",
            "recommendations",
            "performance_insights",
        }:
            return self.performance_recommendations(
                channel_id=channel_id,
            )
        if action in {
            "intelligence_with_analytics",
            "combined_intelligence",
            "intelligence_analytics",
        }:
            return self.intelligence_with_analytics(
                channel_id=channel_id,
            )
        if action in {
            "post_publish",
            "analytics",
            "performance",
        }:
            if video_id is None:
                return {
                    "success": False,
                    "error": "video_id is required",
                }
            return self.post_publish(
                video_id
            )
        if action in {
            "learn",
            "self_learning",
        }:
            if channel_db_id is None:
                return {
                    "success": False,
                    "error": "channel_db_id is required",
                }
            return self.learn(
                channel_db_id
            )
        return {
            "success": False,
            "error": "Unknown YouTube autopilot action",
            "supported_actions": [
                "overview",
                "plan_video",
                "experiment",
                "intelligence_with_analytics",
                "performance_recommendations",
                "next_shorts_plan",
                "post_publish",
                "learn",
            ],
        }
youtube_autopilot = YouTubeAutopilot()
def youtube_autopilot_command(
    action: str,
    **kwargs,
):
    return youtube_autopilot.command(
        action,
        **kwargs,
    )






