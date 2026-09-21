#!/usr/bin/env python3
"""vaultos_health 검증.

REQ-LINT-001 / REQ-LINT-002 / REQ-LINT-003의 acceptance를 픽스처로 확인한다.
표준 라이브러리만 사용한다 (TC-002).
"""

import os
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import vaultos_health as vh  # noqa: E402


def build_vault(base, profile="personal-full", with_all_roots=True):
    """최소한으로 정상인 볼트 픽스처를 만든다."""
    roots = vh.REQUIRED_ROOTS if with_all_roots else vh.REQUIRED_ROOTS[:-1]
    for r in roots:
        os.makedirs(os.path.join(base, r), exist_ok=True)
    for doc in vh.REQUIRED_SYSTEM_DOCS + vh.REQUIRED_GOVERNANCE_DOCS:
        path = os.path.join(base, doc)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        open(path, "w", encoding="utf-8").write("# stub\n")
    proj = os.path.join(base, "02_WORKSPACES", "personal", "projects", "demo")
    os.makedirs(os.path.join(proj, "governance"), exist_ok=True)
    os.makedirs(os.path.join(proj, "requirements"), exist_ok=True)
    open(os.path.join(proj, "project.yaml"), "w", encoding="utf-8").write(
        f"governance_profile: {profile}\n")
    open(os.path.join(proj, "governance", "constitution.md"), "w", encoding="utf-8").write("# c\n")
    open(os.path.join(proj, "requirements", "requirements.yaml"), "w", encoding="utf-8").write(
        "requirements: []\n")
    os.makedirs(os.path.join(proj, "status"), exist_ok=True)
    open(os.path.join(proj, "status", "current-state.yaml"), "w", encoding="utf-8").write(
        "phase: implementation\n")
    return base


def run(base, include_archive=False):
    report = vh.Report()
    notes, by_basename, root_files, all_files = vh.scan_vault(base)
    vh.check_root_structure(base, root_files, report)
    vh.check_links(base, notes, by_basename, all_files, report, include_archive)
    counts = vh.check_projects(base, report)
    return report, counts


def messages(report, check):
    return [m for _, c, m in report.items if c == check]


class RootStructure(unittest.TestCase):
    """REQ-LINT-001"""

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmp)

    def test_정상_볼트는_구조_오류가_없다(self):
        build_vault(self.tmp)
        report, _ = run(self.tmp)
        self.assertEqual(messages(report, "root-structure"), [])
        self.assertEqual(messages(report, "required-doc"), [])

    def test_루트_폴더가_없으면_오류로_검출된다(self):
        build_vault(self.tmp, with_all_roots=False)
        report, _ = run(self.tmp)
        self.assertEqual(len(messages(report, "root-structure")), 1)
        self.assertIn("99_ARCHIVE", messages(report, "root-structure")[0])

    def test_VAULTOS_md가_없으면_오류로_검출된다(self):
        build_vault(self.tmp)
        os.remove(os.path.join(self.tmp, "00_SYSTEM", "VAULTOS.md"))
        report, _ = run(self.tmp)
        self.assertTrue(any("VAULTOS.md" in m for m in messages(report, "required-doc")))

    def test_루트_loose_file은_경고다(self):
        build_vault(self.tmp)
        open(os.path.join(self.tmp, "메모.md"), "w", encoding="utf-8").write("x")
        report, _ = run(self.tmp)
        self.assertTrue(any("메모.md" in m for m in messages(report, "root-loose-file")))

    def test_허용된_루트_파일은_경고하지_않는다(self):
        build_vault(self.tmp)
        for allowed in ("CLAUDE.md", "AGENTS.md", "GEMINI.md"):
            open(os.path.join(self.tmp, allowed), "w", encoding="utf-8").write("x")
        report, _ = run(self.tmp)
        self.assertEqual(messages(report, "root-loose-file"), [])


class Links(unittest.TestCase):
    """REQ-LINT-002"""

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmp)
        build_vault(self.tmp)
        self.note = os.path.join(self.tmp, "03_KNOWLEDGE", "note.md")
        os.makedirs(os.path.dirname(self.note), exist_ok=True)

    def write(self, body):
        open(self.note, "w", encoding="utf-8").write(body)

    def test_존재하는_경로_링크는_통과한다(self):
        self.write("[[00_SYSTEM/VAULTOS|VAULTOS]]\n")
        report, _ = run(self.tmp)
        self.assertEqual(messages(report, "broken-link"), [])

    def test_없는_경로_링크는_오류다(self):
        self.write("[[00_SYSTEM/없는문서|X]]\n")
        report, _ = run(self.tmp)
        self.assertEqual(len(messages(report, "broken-link")), 1)

    def test_표_이스케이프를_오탐하지_않는다(self):
        self.write("| a | [[00_SYSTEM/VAULTOS\\|VAULTOS]] |\n")
        report, _ = run(self.tmp)
        self.assertEqual(messages(report, "broken-link"), [])

    def test_템플릿_치환자를_오탐하지_않는다(self):
        self.write("[[05_OPERATIONS/{{date:YYYY-MM-DD}}]]\n")
        report, _ = run(self.tmp)
        self.assertEqual(messages(report, "broken-link"), [])

    def test_파일명_링크는_폴더가_달라도_해석된다(self):
        self.write("[[VAULTOS]]\n")
        report, _ = run(self.tmp)
        self.assertEqual(messages(report, "broken-link"), [])
        self.assertEqual(messages(report, "unwritten-note"), [])

    def test_미작성_노트는_오류가_아니라_note다(self):
        self.write("[[아직 안 쓴 개념]]\n")
        report, _ = run(self.tmp)
        self.assertEqual(messages(report, "broken-link"), [])
        self.assertEqual(len(messages(report, "unwritten-note")), 1)

    def test_아카이브는_기본_제외된다(self):
        arc = os.path.join(self.tmp, "99_ARCHIVE", "old.md")
        open(arc, "w", encoding="utf-8").write("[[000_VaultOS/02_HOME|옛경로]]\n")
        report, _ = run(self.tmp)
        self.assertEqual(messages(report, "broken-link"), [])
        report2, _ = run(self.tmp, include_archive=True)
        self.assertEqual(len(messages(report2, "broken-link")), 1)

    def test_인라인_코드_안의_링크는_무시한다(self):
        """ISSUE-002 회귀. Obsidian은 백틱 안의 [[...]]를 링크로 해석하지 않는다."""
        self.write("예시: `[[00_SYSTEM/없는문서]]` 는 링크가 아니다\n")
        report, _ = run(self.tmp)
        self.assertEqual(messages(report, "broken-link"), [])

    def test_코드_펜스_안의_링크는_무시한다(self):
        """ISSUE-002 회귀."""
        self.write("```\n[[00_SYSTEM/없는문서]]\n[[또다른/없는것]]\n```\n")
        report, _ = run(self.tmp)
        self.assertEqual(messages(report, "broken-link"), [])

    def test_코드_밖의_링크는_여전히_검출한다(self):
        """ISSUE-002 수정이 정상 검출을 망가뜨리지 않았는지."""
        self.write("`[[안전/예시]]`\n\n[[00_SYSTEM/진짜없음|X]]\n")
        report, _ = run(self.tmp)
        msgs = messages(report, "broken-link")
        self.assertEqual(len(msgs), 1, msgs)
        self.assertIn("진짜없음", msgs[0])

    def test_상대경로_링크를_해석한다(self):
        self.write("[[../00_SYSTEM/VAULTOS|상대]]\n")
        report, _ = run(self.tmp)
        self.assertEqual(messages(report, "broken-link"), [])


class ProjectHub(unittest.TestCase):
    """REQ-LINT-003"""

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmp)

    def test_정상_프로젝트는_통과하고_파일수를_보고한다(self):
        build_vault(self.tmp)
        report, counts = run(self.tmp)
        self.assertEqual(messages(report, "project-hub"), [])
        self.assertEqual(len(counts), 1)
        self.assertEqual(counts[0][0], "personal/demo")
        self.assertGreater(counts[0][1], 0)

    def test_project_yaml이_없으면_오류다(self):
        build_vault(self.tmp)
        os.remove(os.path.join(self.tmp, "02_WORKSPACES", "personal", "projects",
                               "demo", "project.yaml"))
        report, _ = run(self.tmp)
        self.assertTrue(any("project.yaml 없음" in m for m in messages(report, "project-hub")))

    def test_유효하지_않은_프로필은_오류다(self):
        build_vault(self.tmp, profile="아무거나")
        report, _ = run(self.tmp)
        self.assertTrue(any("유효하지 않음" in m for m in messages(report, "project-hub")))

    def test_프로필이_요구하는_파일_부재를_보고한다(self):
        build_vault(self.tmp, profile="personal-full")
        os.remove(os.path.join(self.tmp, "02_WORKSPACES", "personal", "projects",
                               "demo", "governance", "constitution.md"))
        report, _ = run(self.tmp)
        self.assertTrue(any("constitution.md" in m for m in messages(report, "project-hub")))

    def test_personal_light는_project_yaml_하나면_통과한다(self):
        """출처: 01_GOVERNANCE/project-policy.md §2.
        시작 마찰을 낮추는 것이 목적이므로 경량 프로필에 추가 파일을 요구하지 않는다."""
        build_vault(self.tmp, profile="personal-light")
        proj = os.path.join(self.tmp, "02_WORKSPACES", "personal", "projects", "demo")
        os.remove(os.path.join(proj, "status", "current-state.yaml"))
        os.remove(os.path.join(proj, "requirements", "requirements.yaml"))
        os.remove(os.path.join(proj, "governance", "constitution.md"))
        report, _ = run(self.tmp)
        self.assertEqual(messages(report, "project-hub"), [])

    def test_personal_full은_requirements까지_요구한다(self):
        build_vault(self.tmp, profile="personal-full")
        proj = os.path.join(self.tmp, "02_WORKSPACES", "personal", "projects", "demo")
        os.remove(os.path.join(proj, "requirements", "requirements.yaml"))
        report, _ = run(self.tmp)
        self.assertTrue(any("requirements.yaml" in m for m in messages(report, "project-hub")))

    def test_company에_personal_프로필이면_경계_위반이다(self):
        build_vault(self.tmp)
        src = os.path.join(self.tmp, "02_WORKSPACES", "personal", "projects", "demo")
        dst = os.path.join(self.tmp, "02_WORKSPACES", "company", "projects", "leak")
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copytree(src, dst)
        report, _ = run(self.tmp)
        self.assertTrue(any("personal 프로필" in m for m in messages(report, "workspace-boundary")))


if __name__ == "__main__":
    unittest.main(verbosity=2)
