"""
nodes/all_nodes.py - All workflow node implementations
Includes: Node1 (parse), Node2 (search), Node3 (synthesize), Node4 (report)
"""

from typing import List, Dict, Optional
import re
from datetime import datetime
from state import ResearchState, SearchStrategy, Source, Finding
from tools_all import ToolFactory
from utils_logger import get_logger
from utils_error_handler import ResearchAgentError, ErrorHandler

logger = get_logger('research_agent')

# ============================================================================
# NODE 1: PARSE RESEARCH TOPIC
# ============================================================================

class Node1ParseTopic:
    """Parse research topic into search strategy"""
    
    @staticmethod
    def execute(state: ResearchState, error_handler: ErrorHandler) -> bool:
        """
        Parse user input and extract search keywords.
        
        Args:
            state: Current agent state
            error_handler: Error handler instance
        
        Returns:
            Success boolean
        """
        try:
            logger.info("="*60)
            logger.info("NODE 1: PARSE RESEARCH TOPIC")
            logger.info("="*60)
            
            state.current_node = "Node1"
            
            if not state.research_topic or len(state.research_topic.strip()) == 0:
                raise ValueError("Research topic cannot be empty")
            
            logger.info(f"Topic: {state.research_topic}")
            
            # Extract keywords
            state.search_keywords = Node1ParseTopic._extract_keywords(
                state.research_topic
            )
            logger.info(f"Keywords extracted: {state.search_keywords}")
            
            # Identify subtopics
            state.subtopics = Node1ParseTopic._extract_subtopics(
                state.research_topic
            )
            logger.info(f"Subtopics identified: {state.subtopics}")
            
            # Create search strategy
            state.search_strategy = SearchStrategy(
                primary_keywords=state.search_keywords[:2],
                secondary_keywords=state.search_keywords[2:],
                subtopics=state.subtopics,
                search_depth=3,
                max_sources=10
            )
            
            state.add_log("INFO", "Node1", f"Parsed topic into {len(state.search_keywords)} keywords")
            state.nodes_completed.append("Node1")
            
            logger.info("✓ Node 1 completed successfully")
            logger.info("-"*60 + "\n")
            return True
        
        except Exception as e:
            error_handler.handle(e, "Node1: Parse Topic", recoverable=False)
            state.add_error("ParseError", str(e), "Node1")
            logger.error(f"✗ Node 1 failed: {e}")
            return False
    
    @staticmethod
    def _extract_keywords(topic: str) -> List[str]:
        """Extract meaningful keywords from topic"""
        # Remove common words
        stopwords = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 
            'for', 'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'be'
        }
        
        # Split and clean
        words = [w.lower() for w in topic.split() if w.lower() not in stopwords]
        
        # Keep words longer than 3 characters
        keywords = [w for w in words if len(w) > 3]
        
        return keywords[:5]  # Return top 5 keywords
    
    @staticmethod
    def _extract_subtopics(topic: str) -> List[str]:
        """Extract potential subtopics from main topic"""
        # Simple heuristic: look for phrases in parentheses or after key indicators
        subtopics = []
        
        # Look for items in parentheses
        paren_matches = re.findall(r'\(([^)]+)\)', topic)
        subtopics.extend(paren_matches)
        
        # Common subtopic indicators
        indicators = ['aspects of', 'types of', 'forms of', 'examples of']
        for indicator in indicators:
            if indicator in topic.lower():
                parts = topic.lower().split(indicator)
                if len(parts) > 1:
                    subtopic = parts[1].split(',')[0].strip()
                    if subtopic:
                        subtopics.append(subtopic)
        
        # Return top 3 subtopics
        return subtopics[:3] if subtopics else ['General', 'Impact', 'Future']


# ============================================================================
# NODE 2: MULTI-SOURCE SEARCH
# ============================================================================

class Node2Search:
    """Search multiple sources and fetch content"""
    
    @staticmethod
    def execute(state: ResearchState, error_handler: ErrorHandler) -> bool:
        """
        Search multiple sources and fetch their content.
        
        Args:
            state: Current agent state
            error_handler: Error handler instance
        
        Returns:
            Success boolean
        """
        try:
            logger.info("="*60)
            logger.info("NODE 2: MULTI-SOURCE SEARCH")
            logger.info("="*60)
            
            state.current_node = "Node2"
            
            # Get tools
            search_tool = ToolFactory.get_search_tool(use_mock=False)
            fetch_tool = ToolFactory.get_fetch_tool()
            credibility_tool = ToolFactory.get_credibility_tool()
            
            state.raw_sources = []
            
            # Search for each keyword
            for keyword in state.search_keywords:
                logger.info(f"\nSearching for: {keyword}")
                
                try:
                    # Perform search
                    search_results = search_tool.search(keyword, max_results=5)
                    logger.info(f"Found {len(search_results)} results")
                    
                    for i, result in enumerate(search_results):
                        try:
                            logger.info(f"  [{i+1}] Fetching: {result.get('title', 'Unknown')[:60]}...")
                            
                            # Fetch content
                            content, success = fetch_tool.fetch_and_parse(result.get('url', ''))
                            
                            if not content:
                                logger.warning(f"      ⚠ No content fetched")
                                state.sources_failed += 1
                                continue
                            
                            # Score credibility
                            credibility = credibility_tool.score(
                                result.get('url', ''),
                                result.get('domain', ''),
                                content
                            )
                            
                            # Create source object
                            source = Source(
                                url=result.get('url', ''),
                                title=result.get('title', 'Unknown'),
                                content=content,
                                credibility_score=credibility,
                                domain=result.get('domain', ''),
                                author=result.get('author', ''),
                                publish_date=result.get('publish_date', ''),
                                fetch_status='success'
                            )
                            
                            state.raw_sources.append(source)
                            state.sources_searched += 1
                            
                            logger.info(f"      ✓ Added (credibility: {credibility:.2f})")
                        
                        except Exception as e:
                            logger.warning(f"      ⚠ Error fetching result: {e}")
                            state.sources_failed += 1
                            continue
                
                except Exception as e:
                    logger.warning(f"  ⚠ Error searching '{keyword}': {e}")
                    error_handler.handle(e, f"Search: {keyword}", recoverable=True)
                    continue
            
            # Validate we found sources
            if not state.raw_sources:
                logger.warning("✗ No sources found")
                state.add_log("WARNING", "Node2", "No sources found")
                return False
            
            logger.info(f"\n✓ Fetched {len(state.raw_sources)} sources")
            state.add_log("INFO", "Node2", f"Fetched {len(state.raw_sources)} sources")
            state.nodes_completed.append("Node2")
            
            logger.info("-"*60 + "\n")
            return True
        
        except Exception as e:
            error_handler.handle(e, "Node2: Search", recoverable=False)
            state.add_error("SearchError", str(e), "Node2")
            logger.error(f"✗ Node 2 failed: {e}")
            return False


# ============================================================================
# NODE 3: ANALYZE & SYNTHESIZE
# ============================================================================

class Node3Synthesize:
    """Analyze sources and synthesize findings"""
    
    @staticmethod
    def execute(state: ResearchState, error_handler: ErrorHandler) -> bool:
        """
        Analyze sources and extract key findings.
        
        Args:
            state: Current agent state
            error_handler: Error handler instance
        
        Returns:
            Success boolean
        """
        try:
            logger.info("="*60)
            logger.info("NODE 3: ANALYZE & SYNTHESIZE")
            logger.info("="*60)
            
            state.current_node = "Node3"
            
            findings = []
            
            # Extract claims from each source
            for idx, source in enumerate(state.raw_sources):
                logger.info(f"Analyzing [{idx+1}/{len(state.raw_sources)}]: {source.title[:50]}...")
                
                try:
                    # Extract claims/sentences
                    claims = Node3Synthesize._extract_claims(source.content)
                    logger.info(f"  Extracted {len(claims)} claims")
                    
                    for claim in claims[:3]:  # Limit to 3 per source
                        # Calculate confidence
                        confidence = min(source.credibility_score + 0.1, 1.0)
                        
                        # Check for conflicts
                        conflicts = []
                        for existing_finding in findings:
                            if Node3Synthesize._claims_conflict(claim, existing_finding.claim):
                                conflicts.append(existing_finding.claim)
                        
                        # Create finding
                        finding = Finding(
                            claim=claim,
                            supporting_sources=[idx],
                            confidence=confidence,
                            conflicts=conflicts,
                            topic_category=Node3Synthesize._categorize_claim(claim),
                            evidence_count=1
                        )
                        findings.append(finding)
                
                except Exception as e:
                    logger.warning(f"  ⚠ Error analyzing source: {e}")
                    error_handler.handle(e, f"Analyze: {source.url}", recoverable=True)
                    continue
            
            # Merge and deduplicate findings
            state.synthesized_findings = Node3Synthesize._merge_findings(findings)
            
            # Extract themes
            state.themes = Node3Synthesize._extract_themes(
                [f.claim for f in state.synthesized_findings]
            )
            
            logger.info(f"\n✓ Synthesized {len(state.synthesized_findings)} findings")
            logger.info(f"  Themes identified: {state.themes}")
            
            state.add_log("INFO", "Node3", f"Synthesized {len(state.synthesized_findings)} findings")
            state.nodes_completed.append("Node3")
            
            logger.info("-"*60 + "\n")
            return True
        
        except Exception as e:
            error_handler.handle(e, "Node3: Synthesize", recoverable=True)
            state.add_error("SynthesisError", str(e), "Node3")
            logger.warning(f"⚠ Node 3 partial failure: {e}")
            return len(state.synthesized_findings) > 0  # Success if we have any findings
    
    @staticmethod
    def _extract_claims(content: str) -> List[str]:
        """Extract key claims from content"""
        # Simple approach: split by periods and filter
        sentences = content.split('.')
        claims = []
        
        for sentence in sentences:
            cleaned = sentence.strip()
            # Keep sentences that are 20-200 characters (reasonable claim length)
            if 20 < len(cleaned) < 200:
                claims.append(cleaned)
        
        return claims[:5]  # Return top 5
    
    @staticmethod
    def _claims_conflict(claim1: str, claim2: str) -> bool:
        """Check if two claims conflict"""
        # Very simple: look for negation differences
        claim1_lower = claim1.lower()
        claim2_lower = claim2.lower()
        
        # If one has "not" or "no" and the other doesn't, possible conflict
        conflict_indicators = ['not', 'no', 'never', 'cannot', "doesn't"]
        
        claim1_has_negation = any(ind in claim1_lower for ind in conflict_indicators)
        claim2_has_negation = any(ind in claim2_lower for ind in conflict_indicators)
        
        # Check if they're about similar topics but opposite conclusions
        return claim1_has_negation != claim2_has_negation and len(claim1) > 20
    
    @staticmethod
    def _categorize_claim(claim: str) -> str:
        """Categorize a claim by topic"""
        claim_lower = claim.lower()
        
        categories = {
            'Impact': ['impact', 'effect', 'result', 'cause', 'lead'],
            'Statistics': ['percent', '%', 'billion', 'million', 'number', 'amount'],
            'Technology': ['technology', 'develop', 'innovat', 'system', 'method'],
            'Policy': ['policy', 'government', 'law', 'regulation', 'rule'],
            'Economic': ['cost', 'economic', 'financial', 'market', 'price']
        }
        
        for category, keywords in categories.items():
            if any(kw in claim_lower for kw in keywords):
                return category
        
        return 'General'
    
    @staticmethod
    def _merge_findings(findings: List[Finding]) -> List[Finding]:
        """Merge similar findings"""
        if not findings:
            return []
        
        # Simple deduplication: keep unique claims
        merged = []
        seen_claims = set()
        
        for finding in findings:
            claim_key = finding.claim[:50]  # Use first 50 chars as key
            if claim_key not in seen_claims:
                merged.append(finding)
                seen_claims.add(claim_key)
        
        return merged
    
    @staticmethod
    def _extract_themes(claims: List[str]) -> List[str]:
        """Extract main themes from claims"""
        themes = set()
        
        theme_keywords = {
            'Growth & Expansion': ['grow', 'expand', 'increase', 'rise', 'develop'],
            'Challenges': ['challenge', 'problem', 'difficult', 'obstacle', 'issue'],
            'Solutions': ['solution', 'approach', 'method', 'strategy', 'way'],
            'Investment': ['invest', 'fund', 'capital', 'cost', 'spend'],
            'Technology': ['technolog', 'innovat', 'develop', 'system', 'artificial']
        }
        
        for claim in claims:
            claim_lower = claim.lower()
            for theme, keywords in theme_keywords.items():
                if any(kw in claim_lower for kw in keywords):
                    themes.add(theme)
        
        return list(themes)[:5]


# ============================================================================
# NODE 4: REPORT GENERATION
# ============================================================================

class Node4Report:
    """Generate formatted research report"""
    
    @staticmethod
    def execute(state: ResearchState, error_handler: ErrorHandler) -> bool:
        """
        Generate final research report.
        
        Args:
            state: Current agent state
            error_handler: Error handler instance
        
        Returns:
            Success boolean
        """
        try:
            logger.info("="*60)
            logger.info("NODE 4: GENERATE REPORT")
            logger.info("="*60)
            
            state.current_node = "Node4"
            
            # Get citation tool
            citation_tool = ToolFactory.get_citation_tool()
            
            report_parts = []
            
            # Title
            report_parts.append(f"# {state.research_topic}\n")
            report_parts.append(f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n")
            
            if state.themes:
                report_parts.append(f"\n**Key Themes:** {', '.join(state.themes)}\n")
            
            # Organize findings by category
            logger.info(f"Organizing {len(state.synthesized_findings)} findings...")
            
            by_category = {}
            for finding in state.synthesized_findings:
                cat = finding.topic_category
                if cat not in by_category:
                    by_category[cat] = []
                by_category[cat].append(finding)
            
            # Write each category
            for category in sorted(by_category.keys()):
                report_parts.append(f"\n## {category}\n")
                
                for finding in by_category[category]:
                    # Claim
                    report_parts.append(f"- {finding.claim}\n")
                    
                    # Confidence indicator
                    confidence_percent = int(finding.confidence * 100)
                    bar_length = int(finding.confidence * 5)
                    bar = "█" * bar_length + "░" * (5 - bar_length)
                    report_parts.append(f"  *Confidence: {bar} ({confidence_percent}%)*\n")
                    
                    # Citations
                    if finding.supporting_sources:
                        citations = []
                        for source_idx in finding.supporting_sources:
                            if source_idx < len(state.raw_sources):
                                source = state.raw_sources[source_idx]
                                citation = citation_tool.generate(source)
                                citations.append(citation)
                        
                        if citations:
                            report_parts.append(f"  *Sources:* {', '.join(citations)}\n")
                    
                    # Conflicts
                    if finding.conflicts:
                        report_parts.append(f"  ⚠️ *Conflicting information exists*\n")
            
            # Sources section
            report_parts.append(f"\n## Sources ({len(state.raw_sources)})\n")
            
            for i, source in enumerate(state.raw_sources, 1):
                credibility_str = f"{source.credibility_score:.0%}"
                report_parts.append(
                    f"{i}. [{source.title}]({source.url}) "
                    f"(credibility: {credibility_str})\n"
                )
            
            state.final_report = "".join(report_parts)
            
            # Generate metadata
            from utils_logger import get_logger
            avg_confidence = sum(f.confidence for f in state.synthesized_findings) / len(state.synthesized_findings) if state.synthesized_findings else 0
            
            from state import ReportMetadata
            state.report_metadata = ReportMetadata(
                generated_at=datetime.now().isoformat(),
                sources_count=len(state.raw_sources),
                findings_count=len(state.synthesized_findings),
                average_confidence=avg_confidence,
                high_confidence_findings=sum(1 for f in state.synthesized_findings if f.confidence > 0.75),
                conflicting_claims_count=sum(len(f.conflicts) for f in state.synthesized_findings)
            )
            
            logger.info(f"✓ Report generated ({len(state.final_report)} characters)")
            state.add_log("INFO", "Node4", "Report generated successfully")
            state.nodes_completed.append("Node4")
            
            logger.info("-"*60 + "\n")
            return True
        
        except Exception as e:
            error_handler.handle(e, "Node4: Report Generation", recoverable=True)
            state.add_error("ReportError", str(e), "Node4")
            logger.warning(f"⚠ Node 4 failed: {e}")
            return False
