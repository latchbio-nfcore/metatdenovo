from dataclasses import dataclass
from enum import Enum
import os
import subprocess
import requests
import shutil
from pathlib import Path
import typing
import typing_extensions

from latch.resources.workflow import workflow
from latch.resources.tasks import nextflow_runtime_task, custom_task
from latch.types.file import LatchFile
from latch.types.directory import LatchDir, LatchOutputDir
from latch.ldata.path import LPath
from latch_cli.nextflow.workflow import get_flag
from latch_cli.nextflow.utils import _get_execution_name
from latch_cli.utils import urljoins
from latch.types import metadata
from flytekit.core.annotation import FlyteAnnotation

from latch_cli.services.register.utils import import_module_by_path

meta = Path("latch_metadata") / "__init__.py"
import_module_by_path(meta)
import latch_metadata

@custom_task(cpu=0.25, memory=0.5, storage_gib=1)
def initialize() -> str:
    token = os.environ.get("FLYTE_INTERNAL_EXECUTION_ID")
    if token is None:
        raise RuntimeError("failed to get execution token")

    headers = {"Authorization": f"Latch-Execution-Token {token}"}

    print("Provisioning shared storage volume... ", end="")
    resp = requests.post(
        "http://nf-dispatcher-service.flyte.svc.cluster.local/provision-storage",
        headers=headers,
        json={
            "storage_gib": 100,
        }
    )
    resp.raise_for_status()
    print("Done.")

    return resp.json()["name"]






@nextflow_runtime_task(cpu=4, memory=8, storage_gib=100)
def nextflow_runtime(pvc_name: str, input: LatchFile, se_reads: typing.Optional[bool], outdir: typing_extensions.Annotated[LatchDir, FlyteAnnotation({'output': True})], email: typing.Optional[str], multiqc_title: typing.Optional[str], skip_qc: typing.Optional[bool], skip_fastqc: typing.Optional[bool], clip_r1: typing.Optional[str], clip_r2: typing.Optional[str], three_prime_clip_r1: typing.Optional[str], three_prime_clip_r2: typing.Optional[str], save_trimmed: typing.Optional[bool], trim_nextseq: typing.Optional[str], skip_trimming: typing.Optional[bool], sequence_filter: typing.Optional[str], bbnorm: typing.Optional[bool], save_bbnorm_fastq: typing.Optional[bool], assembly: typing.Optional[LatchFile], save_bam: typing.Optional[bool], save_samtools: typing.Optional[bool], protein_fasta: typing.Optional[str], gff: typing.Optional[str], prodigal_trainingfile: typing.Optional[str], hmmdir: typing.Optional[LatchDir], hmmfiles: typing.Optional[LatchFile], eukulele_db: typing.Optional[str], multiqc_methods_description: typing.Optional[str], bbnorm_target: typing.Optional[int], bbnorm_min: typing.Optional[int], assembler: typing.Optional[str], min_contig_length: typing.Optional[int], orf_caller: typing.Optional[str], skip_eggnog: typing.Optional[bool], eggnog_dbpath: typing.Optional[str], skip_kofamscan: typing.Optional[bool], kofam_dir: typing.Optional[str], hmmpattern: typing.Optional[str], skip_eukulele: typing.Optional[bool], eukulele_method: typing.Optional[str], eukulele_dbpath: typing.Optional[str]) -> None:
    try:
        shared_dir = Path("/nf-workdir")



        ignore_list = [
            "latch",
            ".latch",
            "nextflow",
            ".nextflow",
            "work",
            "results",
            "miniconda",
            "anaconda3",
            "mambaforge",
        ]

        shutil.copytree(
            Path("/root"),
            shared_dir,
            ignore=lambda src, names: ignore_list,
            ignore_dangling_symlinks=True,
            dirs_exist_ok=True,
        )

        cmd = [
            "/root/nextflow",
            "run",
            str(shared_dir / "main.nf"),
            "-work-dir",
            str(shared_dir),
            "-profile",
            "docker",
            "-c",
            "latch.config",
                *get_flag('input', input),
                *get_flag('se_reads', se_reads),
                *get_flag('outdir', outdir),
                *get_flag('email', email),
                *get_flag('multiqc_title', multiqc_title),
                *get_flag('skip_qc', skip_qc),
                *get_flag('skip_fastqc', skip_fastqc),
                *get_flag('clip_r1', clip_r1),
                *get_flag('clip_r2', clip_r2),
                *get_flag('three_prime_clip_r1', three_prime_clip_r1),
                *get_flag('three_prime_clip_r2', three_prime_clip_r2),
                *get_flag('save_trimmed', save_trimmed),
                *get_flag('trim_nextseq', trim_nextseq),
                *get_flag('skip_trimming', skip_trimming),
                *get_flag('sequence_filter', sequence_filter),
                *get_flag('bbnorm', bbnorm),
                *get_flag('bbnorm_target', bbnorm_target),
                *get_flag('bbnorm_min', bbnorm_min),
                *get_flag('save_bbnorm_fastq', save_bbnorm_fastq),
                *get_flag('assembler', assembler),
                *get_flag('assembly', assembly),
                *get_flag('min_contig_length', min_contig_length),
                *get_flag('save_bam', save_bam),
                *get_flag('save_samtools', save_samtools),
                *get_flag('protein_fasta', protein_fasta),
                *get_flag('gff', gff),
                *get_flag('orf_caller', orf_caller),
                *get_flag('prodigal_trainingfile', prodigal_trainingfile),
                *get_flag('skip_eggnog', skip_eggnog),
                *get_flag('eggnog_dbpath', eggnog_dbpath),
                *get_flag('skip_kofamscan', skip_kofamscan),
                *get_flag('kofam_dir', kofam_dir),
                *get_flag('hmmdir', hmmdir),
                *get_flag('hmmfiles', hmmfiles),
                *get_flag('hmmpattern', hmmpattern),
                *get_flag('skip_eukulele', skip_eukulele),
                *get_flag('eukulele_method', eukulele_method),
                *get_flag('eukulele_db', eukulele_db),
                *get_flag('eukulele_dbpath', eukulele_dbpath),
                *get_flag('multiqc_methods_description', multiqc_methods_description)
        ]

        print("Launching Nextflow Runtime")
        print(' '.join(cmd))
        print(flush=True)

        env = {
            **os.environ,
            "NXF_HOME": "/root/.nextflow",
            "NXF_OPTS": "-Xms2048M -Xmx8G -XX:ActiveProcessorCount=4",
            "K8S_STORAGE_CLAIM_NAME": pvc_name,
            "NXF_DISABLE_CHECK_LATEST": "true",
        }
        subprocess.run(
            cmd,
            env=env,
            check=True,
            cwd=str(shared_dir),
        )
    finally:
        print()

        nextflow_log = shared_dir / ".nextflow.log"
        if nextflow_log.exists():
            name = _get_execution_name()
            if name is None:
                print("Skipping logs upload, failed to get execution name")
            else:
                remote = LPath(urljoins("latch:///your_log_dir/nf_nf_core_metatdenovo", name, "nextflow.log"))
                print(f"Uploading .nextflow.log to {remote.path}")
                remote.upload_from(nextflow_log)



@workflow(metadata._nextflow_metadata)
def nf_nf_core_metatdenovo(input: LatchFile, se_reads: typing.Optional[bool], outdir: typing_extensions.Annotated[LatchDir, FlyteAnnotation({'output': True})], email: typing.Optional[str], multiqc_title: typing.Optional[str], skip_qc: typing.Optional[bool], skip_fastqc: typing.Optional[bool], clip_r1: typing.Optional[str], clip_r2: typing.Optional[str], three_prime_clip_r1: typing.Optional[str], three_prime_clip_r2: typing.Optional[str], save_trimmed: typing.Optional[bool], trim_nextseq: typing.Optional[str], skip_trimming: typing.Optional[bool], sequence_filter: typing.Optional[str], bbnorm: typing.Optional[bool], save_bbnorm_fastq: typing.Optional[bool], assembly: typing.Optional[LatchFile], save_bam: typing.Optional[bool], save_samtools: typing.Optional[bool], protein_fasta: typing.Optional[str], gff: typing.Optional[str], prodigal_trainingfile: typing.Optional[str], hmmdir: typing.Optional[LatchDir], hmmfiles: typing.Optional[LatchFile], eukulele_db: typing.Optional[str], multiqc_methods_description: typing.Optional[str], bbnorm_target: typing.Optional[int] = 100, bbnorm_min: typing.Optional[int] = 5, assembler: typing.Optional[str] = 'megahit', min_contig_length: typing.Optional[int] = 0, orf_caller: typing.Optional[str] = 'prodigal', skip_eggnog: typing.Optional[bool] = False, eggnog_dbpath: typing.Optional[str] = 'eggnog', skip_kofamscan: typing.Optional[bool] = False, kofam_dir: typing.Optional[str] = './kofam/', hmmpattern: typing.Optional[str] = '*.hmm', skip_eukulele: typing.Optional[bool] = False, eukulele_method: typing.Optional[str] = 'mets', eukulele_dbpath: typing.Optional[str] = './eukulele/') -> None:
    """
    nf-core/metatdenovo

    Sample Description
    """

    pvc_name: str = initialize()
    nextflow_runtime(pvc_name=pvc_name, input=input, se_reads=se_reads, outdir=outdir, email=email, multiqc_title=multiqc_title, skip_qc=skip_qc, skip_fastqc=skip_fastqc, clip_r1=clip_r1, clip_r2=clip_r2, three_prime_clip_r1=three_prime_clip_r1, three_prime_clip_r2=three_prime_clip_r2, save_trimmed=save_trimmed, trim_nextseq=trim_nextseq, skip_trimming=skip_trimming, sequence_filter=sequence_filter, bbnorm=bbnorm, bbnorm_target=bbnorm_target, bbnorm_min=bbnorm_min, save_bbnorm_fastq=save_bbnorm_fastq, assembler=assembler, assembly=assembly, min_contig_length=min_contig_length, save_bam=save_bam, save_samtools=save_samtools, protein_fasta=protein_fasta, gff=gff, orf_caller=orf_caller, prodigal_trainingfile=prodigal_trainingfile, skip_eggnog=skip_eggnog, eggnog_dbpath=eggnog_dbpath, skip_kofamscan=skip_kofamscan, kofam_dir=kofam_dir, hmmdir=hmmdir, hmmfiles=hmmfiles, hmmpattern=hmmpattern, skip_eukulele=skip_eukulele, eukulele_method=eukulele_method, eukulele_db=eukulele_db, eukulele_dbpath=eukulele_dbpath, multiqc_methods_description=multiqc_methods_description)

